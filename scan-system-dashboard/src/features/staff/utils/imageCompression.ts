import imageCompression from 'browser-image-compression'

/**
 * Compress image before upload to reduce file size and improve upload performance
 * 
 * @param file The original image file
 * @param maxWidth Maximum width in pixels (default: 800)
 * @param maxHeight Maximum height in pixels (default: 800)
 * @param maxSizeMB Maximum file size in MB (default: 1)
 * @param quality Image quality 0-1 (default: 0.8)
 * @returns Compressed image file
 */
export async function compressImage(
  file: File,
  options: {
    maxWidth?: number
    maxHeight?: number
    maxSizeMB?: number
    quality?: number
  } = {}
): Promise<File> {
  const {
    maxWidth = 800,
    maxHeight = 800,
    maxSizeMB = 1,
    quality = 0.8,
  } = options

  // If file is already small enough, return as-is
  const fileSizeMB = file.size / (1024 * 1024)
  if (fileSizeMB <= maxSizeMB) {
    return file
  }

  try {
    // Preserve original file extension and name
    const originalName = file.name
    const originalExtension = originalName.split('.').pop()?.toLowerCase() || 'jpg'
    
    // Ensure we use a valid image type that matches backend validation
    // Backend accepts: jpeg, jpg, png, gif, webp, heic, heif
    let outputType = file.type
    if (!outputType || !outputType.startsWith('image/')) {
      // Default to jpeg if type is not recognized
      outputType = 'image/jpeg'
    }
    
    // If original is HEIC/HEIF, convert to JPEG (Cloudinary handles these but browser compression might not)
    if (originalExtension === 'heic' || originalExtension === 'heif') {
      outputType = 'image/jpeg'
    }

    const compressionOptions = {
      maxSizeMB,
      maxWidthOrHeight: Math.max(maxWidth, maxHeight),
      useWebWorker: true, // Use web worker for better performance
      fileType: outputType, // Preserve or set appropriate MIME type
      initialQuality: quality,
      // Preserve the original file name structure
      preserveExif: false, // Remove EXIF data to reduce size
    }

    const compressedResult = await imageCompression(file, compressionOptions)

    // imageCompression returns a File, but ensure it has correct properties
    let compressedFile: File
    
    if (compressedResult instanceof File) {
      // If the name or type changed, create a new File with correct properties
      if (compressedResult.name !== originalName || compressedResult.type !== outputType) {
        compressedFile = new File(
          [compressedResult],
          originalName, // Preserve original filename
          {
            type: outputType, // Ensure correct MIME type
            lastModified: compressedResult.lastModified || Date.now(),
          }
        )
      } else {
        compressedFile = compressedResult
      }
    } else {
      // If it's a Blob (shouldn't happen, but handle it), convert to File
      compressedFile = new File(
        [compressedResult],
        originalName,
        {
          type: outputType,
          lastModified: Date.now(),
        }
      )
    }

    // Validate the file before returning
    if (!compressedFile || compressedFile.size === 0) {
      console.warn('Compressed file is invalid, returning original file')
      return file
    }

    console.log(
      `Image compressed: ${(file.size / (1024 * 1024)).toFixed(2)}MB -> ${(compressedFile.size / (1024 * 1024)).toFixed(2)}MB`,
      `Type: ${compressedFile.type}`,
      `Name: ${compressedFile.name}`,
      `IsFile: ${compressedFile instanceof File}`
    )

    return compressedFile
  } catch (error) {
    console.error('Image compression failed:', error)
    // If compression fails, return original file
    return file
  }
}

