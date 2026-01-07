<?php

namespace App\Domain\v1\Staffs\Services;

use App\Domain\v1\Staffs\Models\Staff;
use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Storage;
use CloudinaryLabs\CloudinaryLaravel\Facades\Cloudinary;

class StaffService
{
    /**
     * Upload profile image to Cloudinary
     * OPTIMIZED: Upload raw image without transformations for maximum speed
     * Transformations are applied on-demand via getOptimizedImageUrl()
     */
    public function uploadProfileImage(?UploadedFile $file): ?string
    {
        if (!$file) {
            return null;
        }

        try {
            // Upload file directly without transformations (much faster)
            // Transformations will be applied on-demand when displaying images
            $uploadedFile = Cloudinary::uploadApi()->upload(
                $file->getRealPath(),
                [
                    'folder' => 'scan-staff-profiles',
                    'public_id' => 'staff_' . time() . '_' . uniqid(),
                    'overwrite' => true,
                    'resource_type' => 'auto',
                    'allowed_formats' => ['jpg', 'jpeg', 'png', 'gif', 'webp', 'heic', 'heif'],
                    
                    // PERFORMANCE: Optimized upload settings
                    'use_filename' => false,       // Don't use original filename (faster)
                    'unique_filename' => true,      // Ensure unique filenames
                    'invalidate' => false,         // Skip CDN cache invalidation (faster)
                ]
            );

            return $uploadedFile['secure_url'] ?? null;
        } catch (\Exception $e) {
            // Log the exact Cloudinary error for troubleshooting
            Log::error('Profile image upload failed', [
                'error' => $e->getMessage(),
                'code' => $e->getCode(),
            ]);
            throw new \Exception('Failed to upload image to Cloudinary: ' . $e->getMessage());
        }
    }

    /**
     * Generate optimized image URL with transformations applied on-demand
     * This allows fast uploads while still getting optimized images when displayed
     * 
     * @param string|null $imageUrl The original Cloudinary URL
     * @param int $width Maximum width (default: 800)
     * @param int $height Maximum height (default: 800)
     * @param string $quality Quality setting (default: 'auto:good')
     * @return string|null Optimized image URL or null if input is null
     */
    public function getOptimizedImageUrl(?string $imageUrl, int $width = 800, int $height = 800, string $quality = 'auto:good'): ?string
    {
        if (!$imageUrl) {
            return null;
        }

        // If it's not a Cloudinary URL, return as-is
        if (!str_contains($imageUrl, 'cloudinary.com')) {
            return $imageUrl;
        }

        // Check if transformations are already applied (avoid double transformation)
        if (preg_match('/\/upload\/[^\/]*(w_\d+|h_\d+|c_|q_)/', $imageUrl)) {
            return $imageUrl; // Already has transformations
        }

        // Build transformation string
        // Format: w_800,h_800,c_limit,q_auto:good
        $transformation = "w_{$width},h_{$height},c_limit,q_{$quality}";
        
        // Cloudinary URL format: https://res.cloudinary.com/{cloud}/image/upload/{version}/{public_id}.{format}
        // We need to insert transformation after '/upload/' and before version or public_id
        // Handle both cases: /upload/v123/... and /upload/...
        $optimizedUrl = preg_replace(
            '/(\/image\/upload\/)(v\d+\/)?/',
            '$1' . $transformation . '/$2',
            $imageUrl,
            1
        );

        return $optimizedUrl ?: $imageUrl; // Fallback to original if regex fails
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
            // 1. Get the path from the URL (e.g., /cloudname/image/upload/v1/folder/img.jpg)
            $path = parse_url($imageUrl, PHP_URL_PATH);

            // 2. Use Regex to capture everything AFTER 'upload/' and 'v12345/' 
            // but BEFORE the file extension (.jpg)
            // This captures "folder/subfolder/filename"
            if (preg_match('/upload\/(?:v\d+\/)?(.+)\.[a-z]{3,4}$/i', $path, $matches)) {
                $publicId = $matches[1];

                // 3. Delete using the full Public ID (including the folder)
                $response = Cloudinary::uploadApi()->destroy($publicId);

                return isset($response['result']) && $response['result'] === 'ok';
            }

            return false;
        } catch (\Exception $e) {
            // Log the error so you can see why it failed in storage/logs/laravel.log
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
