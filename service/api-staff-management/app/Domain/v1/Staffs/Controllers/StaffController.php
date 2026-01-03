<?php

namespace App\Domain\v1\Staffs\Controllers;

use App\Http\Controllers\Controller;
use App\Domain\v1\Staffs\Models\Staff;
use App\Domain\v1\Staffs\Requests\CreateStaffRequest;
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
            ->with([
                'user' => function ($q) {
                    $q->select('id', 'username', 'email')
                        ->with('roles:id,name');
                },
                'office' => fn($q) => $q->select('id', 'name')
            ])
            ->when($request->search, function ($query, $search) {
                $query->where(function ($q) use ($search) {
                    // Ensure these columns are indexed in DB
                    $q->where('full_name', 'like', "{$search}%") //Forward-matching
                        ->orWhere('phone', 'like', "{$search}%");
                });
            })
            ->when($request->office_id, function ($query, $officeId) {
                $query->where('office_id', $officeId);
            })
            ->latest()  // Good to have a predictable order for pagination
            ->paginate($request->get('per_page', 15));

        return response()->json([
            'status' => 'success',
            'data' => $staff->items(),
            'pagination' => [
                'current_page' => $staff->currentPage(),
                'per_page'     => $staff->perPage(),
                'total'        => $staff->total(),
                'last_page'    => $staff->lastPage(),
            ]
        ]);
    }

    // Store
    public function store(CreateStaffRequest $request): JsonResponse
    {
        try {
            DB::beginTransaction();
            // Create User 
            $user = User::create($request->only([
                User::USERNAME,
                User::EMAIL,
                User::PASSWORD
            ]));

            // 2. Assign Role ឱ្យ User (ដូចក្នុង Command របស់អ្នក)
            $user->assignRole($request->role);

            // 2. Prepare staff data that insert in the feild in the CreateStaffRequest
            $staffData = $request->safe()->except([
                User::USERNAME,
                User::EMAIL,
                User::PASSWORD,
                'password_confirmation',
                'role'
            ]);
            $staffData[Staff::USER_ID] = $user->id;


            // 3. Handle Image in the Cloudinary
            if ($request->hasFile(Staff::PROFILE_IMAGE)) {
                $imageUrl = $this->staffService->uploadProfileImage($request->file(Staff::PROFILE_IMAGE));
                $staffData[Staff::PROFILE_IMAGE] = $imageUrl;
            }

            //  4. Create Staff
            $staff = Staff::create($staffData);

            // 5. Load data respone
            $staff->load([
                'user' => fn($q) => $q->select('id', 'username', 'email')->with('roles:id,name'),
                'office' => fn($q) => $q->select('id', 'name')
            ]);

            DB::commit();
            // 6. Respones
            return response()->json([
                'status' => 'success',
                'message' => 'Staff and user created successfully',
                'data' => $staff
            ], 201);;
        } catch (\Exception $e) {
            DB::rollBack();
            return response()->json([
                'status' => 'error',
                'message' => 'Failed to create staff: ' . $e->getMessage()
            ], 500);
        }
    }
    // Update

    // Delete
    public function destroy(int $id): JsonResponse
    {
        try {
            DB::beginTransaction();


            $staff = Staff::findOrFail($id);

            // 3. get User and Image URL from Staff
            $user = $staff->user;
            $imagePath = $staff->profile_image;

            // 4. delete Staff
            $staff->delete();

            // 5. delete User
            if ($user) {
                $user->delete();
            }

            // 6. delete Cloudinary Service (Optional but Recommended)
            if ($imagePath) {
                $this->staffService->deleteProfileImage($imagePath);
            }

            DB::commit();

            return response()->json([
                'status' => 'success',
                'message' => 'Staff, user, and related data deleted successfully'
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
                'message' => 'Failed to delete staff: ' . $e->getMessage()
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
