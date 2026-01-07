<?php

namespace App\Domain\v1\Staffs\Controllers;

use App\Http\Controllers\Controller;
use App\Domain\v1\Staffs\Models\Staff;
use App\Domain\v1\Staffs\Requests\CreateStaffRequest;
use App\Domain\v1\Staffs\Requests\UpdateStaffRequest;
use App\Domain\v1\Staffs\Resources\StaffResource;
use App\Domain\v1\Staffs\Services\StaffService;
use App\Domain\v1\Users\Models\User;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;




class StaffController extends Controller
{
    protected StaffService $staffService;

    public function __construct(StaffService $staffService)
    {
        $this->staffService = $staffService;
    }

    public function index(Request $request)
    {
        $staff = Staff::query()
            ->select('id', 'user_id', 'office_id', 'full_name', 'phone', 'shift_start', 'shift_end', 'join_date')
            ->with([
                'user:id,email,username',
                'user.roles:id,name',
                'office:id,name'
            ])
            ->when($request->search, function ($query, $search) {
                $query->where('full_name', 'like', "{$search}%")
                    ->orWhere('phone', 'like', "{$search}%");
            })
            ->latest()
            ->paginate($request->get('per_page', 15));

        return response()->json([
            'status' => 'success',
            'data' => StaffResource::collection($staff->items()),
            'pagination' => [
                'current_page' => $staff->currentPage(),
                'total'        => $staff->total(),
                'last_page'    => $staff->lastPage(),
            ]
        ]);
    }

    // Store
    public function store(CreateStaffRequest $request): JsonResponse
    {
        // PERFORMANCE: Upload image BEFORE starting transaction
        // This prevents holding the DB transaction open during slow Cloudinary upload
        $imageUrl = null;
        
        try {
            // 1. Handle Image Upload FIRST (outside transaction for better performance)
            if ($request->hasFile(Staff::PROFILE_IMAGE)) {
                $imageUrl = $this->staffService->uploadProfileImage($request->file(Staff::PROFILE_IMAGE));
            }

            // 2. NOW start database transaction (faster since image is already uploaded)
            DB::beginTransaction();
            
            // 3. Create User 
            $user = User::create($request->only([
                User::USERNAME,
                User::EMAIL,
                User::PASSWORD
            ]));

            // 4. Assign Role
            $user->assignRole($request->role);

            // 5. Prepare staff data
            $staffData = $request->safe()->except([
                User::USERNAME,
                User::EMAIL,
                User::PASSWORD,
                'role'
            ]);
            $staffData[Staff::USER_ID] = $user->id;

            // 6. Add uploaded image URL if exists
            if ($imageUrl) {
                $staffData[Staff::PROFILE_IMAGE] = $imageUrl;
            }

            // 7. Create Staff
            $staff = Staff::create($staffData);

            // 8. Load relationships for response
            $staff->load([
                'user' => fn($q) => $q->select('id', 'username', 'email')->with('roles:id,name'),
                'office' => fn($q) => $q->select('id', 'name')
            ]);

            DB::commit();
            
            // 9. Return success response
            return response()->json([
                'status' => 'success',
                'message' => 'Staff and user created successfully',
                'data' => $staff
            ], 201);
            
        } catch (\Exception $e) {
            DB::rollBack();
            
            // CLEANUP: If we uploaded an image but DB failed, delete it from Cloudinary
            if ($imageUrl) {
                $this->staffService->deleteProfileImage($imageUrl);
            }
            
            return response()->json([
                'status' => 'error',
                'message' => 'Failed to create staff: ' . $e->getMessage()
            ], 500);
        }
    }
    // Update
    public function update(UpdateStaffRequest $request, int $id): JsonResponse
    {
        // PERFORMANCE: Handle image upload BEFORE transaction
        $newImageUrl = null;
        $oldImageUrl = null;
        
        try {
            // 1. Find the staff record first
            $staff = Staff::findOrFail($id);
            $user = $staff->user;
            
            # Get current authenticated user (may be null)
            $currentUser = $request->user();

            # if not authenticated, return 401
            if (!$currentUser) {
                return response()->json(['status' => 'error', 'message' => 'Unauthorized'], 401);
            }

            $isAdmin = $currentUser->hasRole('admin');
            
            // 2. Handle Image Upload FIRST (outside transaction for better performance)
            if ($request->hasFile(Staff::PROFILE_IMAGE)) {
                $oldImageUrl = $staff->profile_image; // Store for cleanup
                $newImageUrl = $this->staffService->uploadProfileImage($request->file(Staff::PROFILE_IMAGE));
            }

            // 3. NOW start database transaction
            DB::beginTransaction();
            
            // 4. Update User Account (ADMIN ONLY)
            if ($isAdmin) {
                $userData = $request->only([User::USERNAME, User::EMAIL]);

                if ($request->filled(User::PASSWORD)) {
                    // Hashing here for safety
                    $userData[User::PASSWORD] = bcrypt($request->input(User::PASSWORD));
                }

                if (!empty($userData)) {
                    $user->update($userData);
                }

                // Update Role
                if ($request->has('role')) {
                    $user->syncRoles([$request->role]);
                }
            }

            // 5. Handle Staff Information (Both Staff & Admin)
            // We exclude sensitive user fields so staff can't sneak them in via staffData
            $staffData = $request->safe()->except([
                User::USERNAME,
                User::EMAIL,
                User::PASSWORD,
                'role'
            ]);

            // 6. Add new image URL if uploaded
            if ($newImageUrl) {
                $staffData[Staff::PROFILE_IMAGE] = $newImageUrl;
            }

            $staff->update($staffData);

            $staff->load([
                'user' => fn($q) => $q->select('id', 'username', 'email')->with('roles:id,name'),
                'office' => fn($q) => $q->select('id', 'name')
            ]);

            DB::commit();
            
            // 7. Delete old image AFTER successful commit
            if ($oldImageUrl && $newImageUrl) {
                $this->staffService->deleteProfileImage($oldImageUrl);
            }

            // 8. Return clean response using Resource
            return response()->json([
                'status' => 'success',
                'message' => 'Staff updated successfully',
                'data' => $staff
            ]);
            
        } catch (\Illuminate\Database\Eloquent\ModelNotFoundException $e) {
            // CLEANUP: If we uploaded a new image but update failed, delete it
            if ($newImageUrl) {
                $this->staffService->deleteProfileImage($newImageUrl);
            }
            return response()->json(['status' => 'error', 'message' => 'Staff record not found'], 404);
        } catch (\Exception $e) {
            DB::rollBack();
            
            // CLEANUP: If we uploaded a new image but update failed, delete it
            if ($newImageUrl) {
                $this->staffService->deleteProfileImage($newImageUrl);
            }
            
            return response()->json(['status' => 'error', 'message' => 'Update failed: ' . $e->getMessage()], 500);
        }
    }

    // Delete
    public function destroy(int $id): JsonResponse
    {
        try {
            // 1. Find the record first
            $staff = Staff::findOrFail($id);
            $user = $staff->user;
            $imagePath = $staff->profile_image;

            DB::beginTransaction();

            // 2. Delete the Staff and User from DB
            // We do this inside the transaction
            $staff->delete();
            if ($user) {
                $user->delete();
            }

            // 3. Delete from Cloudinary
            // We do this AFTER the local deletes but BEFORE the commit.
            // Or, you can do it after commit if you don't want a Cloudinary failure 
            // to roll back your database.
            if ($imagePath) {
                $this->staffService->deleteProfileImage($imagePath);
            }

            DB::commit();

            return response()->json([
                'status' => 'success',
                'message' => 'Staff and related data deleted successfully'
            ]);
        } catch (\Illuminate\Database\Eloquent\ModelNotFoundException $e) {
            return response()->json([
                'status' => 'error',
                'message' => 'Staff record not found'
            ], 404);
        } catch (\Exception $e) {
            DB::rollBack();
            return response()->json([
                'status' => 'error',
                'message' => 'Failed to delete: ' . $e->getMessage()
            ], 500);
        }
    }

    /**
     * Test Cloudinary connection
     */
    public function testCloudinary(): JsonResponse
    {
        $result = $this->staffService->testCloudinary();

        $statusCode = $result['status'] === 'success' ? 200 : 500;

        return response()->json($result, $statusCode);
    }
}
