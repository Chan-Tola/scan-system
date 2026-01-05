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
    /**
     * Upload profile image to Cloudinary
     */
    public function uploadProfileImage(?UploadedFile $file): ?string
    {
        if (!$file) {
            return null;
        }

        try {
            // Upload to Cloudinary using Native SDK syntax
            // The facade returns the SDK instance, so we call uploadApi()
            $uploadedFile = Cloudinary::uploadApi()->upload($file->getRealPath(), [
                'folder' => 'scan-staff-profiles',
                'public_id' => 'staff_' . time() . '_' . uniqid(),
                'overwrite' => true,
                'resource_type' => 'image'
            ]);

            return $uploadedFile['secure_url']; 
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

                Cloudinary::uploadApi()->destroy($publicId);
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
    /**
     * Test Cloudinary connection
     */
    public function testCloudinary(): array
    {
        // Create a temporary file
        $tempFile = sys_get_temp_dir() . '/test_image_' . time() . '.txt';
        file_put_contents($tempFile, 'This is a test file for Cloudinary upload.');

        try {
            // Upload the temp file (as "raw" or "auto" since it's text, or pretend it's an image if we really want, but let's stick to auto for safety or just raw)
            // Actually, for image resource type it implies image validation. 
            // Let's make a tiny valid base64 image or just switch resource_type to 'raw' for this test.
            // Or better, let's keep resource_type 'auto' to avoid "empty file" on image check.
            
            $testResult = Cloudinary::uploadApi()->upload(
                $tempFile, 
                [
                    'folder' => 'test',
                    'public_id' => 'test_' . time(),
                    'resource_type' => 'auto' 
                ]
            );

            // Clean up
            @unlink($tempFile);

            return [
                'status' => 'success',
                'message' => 'Cloudinary connection successful',
                'test_url' => $testResult['secure_url'],
                'public_id' => $testResult['public_id']
            ];
        } catch (\Exception $e) {
            // Clean up
            @unlink($tempFile);
            
            return [
                'status' => 'error',
                'message' => 'Cloudinary connection failed: ' . $e->getMessage()
            ];
        }
    }
}
