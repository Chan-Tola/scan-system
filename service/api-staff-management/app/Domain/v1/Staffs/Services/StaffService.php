<?php

namespace App\Domain\v1\Staffs\Services;

use App\Domain\v1\Staffs\Models\Staff;
use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Storage;
use CloudinaryLabs\CloudinaryLaravel\Facades\Cloudinary;

class StaffService
{
    /**
     * Upload profile image to Cloudinary
     */
    public function uploadProfileImage(?UploadedFile $file): ?string
    {
        if (!$file) {
            return null;
        }

        try {
            // Upload to Cloudinary
            $uploadedFileUrl = Cloudinary::upload($file->getRealPath(), [
                'folder' => 'scan-staff-profiles',
                'public_id' => 'staff_' . time() . '_' . uniqid(),
                'overwrite' => true,
                'resource_type' => 'image'
            ])->getSecurePath();

            return $uploadedFileUrl;
        } catch (\Exception $e) {
            throw new \Exception('Failed to upload image to Cloudinary: ' . $e->getMessage());
        }
    }

    /**
     * Delete profile image from Cloudinary
     */
    public function deleteProfileImage(?string $imageUrl): bool
    {
        if (!$imageUrl) {
            return false;
        }

        try {
            // Extract public_id from Cloudinary URL
            $urlParts = parse_url($imageUrl);
            $pathParts = explode('/', trim($urlParts['path'], '/'));

            // Find the upload segment and get public_id
            $uploadIndex = array_search('upload', $pathParts);
            if ($uploadIndex !== false && isset($pathParts[$uploadIndex + 2])) {
                $publicId = $pathParts[$uploadIndex + 2];
                // Remove file extension
                $publicId = pathinfo($publicId, PATHINFO_FILENAME);

                Cloudinary::destroy($publicId);
                return true;
            }

            return false;
        } catch (\Exception $e) {
            return false;
        }
    }

    /**
     * Test Cloudinary connection
     */
    public function testCloudinary(): array
    {
        try {
            // Try to upload a test file (you can create a simple test image)
            $testResult = Cloudinary::upload(
                base_path('public/favicon.ico'), // Using existing file as test
                [
                    'folder' => 'test',
                    'public_id' => 'test_' . time(),
                    'resource_type' => 'image'
                ]
            );

            return [
                'status' => 'success',
                'message' => 'Cloudinary connection successful',
                'test_url' => $testResult->getSecurePath(),
                'public_id' => $testResult->getPublicId()
            ];
        } catch (\Exception $e) {
            return [
                'status' => 'error',
                'message' => 'Cloudinary connection failed: ' . $e->getMessage()
            ];
        }
    }
}
