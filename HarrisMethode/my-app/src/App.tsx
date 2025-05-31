import { useState, useRef } from 'react';

interface ProcessedImages {
  original: string;
  grayscale: string;
  smooth: string;
  gradient: string;
  harris: string;
  angle: string;
  harris_corners: string;
  gftt_corners: string;
  combined_corners: string;
}

function App() {
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [processedImages, setProcessedImages] = useState<ProcessedImages | null>(null);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      // Reset states
      setError(null);
      setProcessedImages(null);
      setSelectedFile(file);

      // Create a preview
      const reader = new FileReader();
      reader.onload = () => {
        setPreviewUrl(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleDragOver = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
  };

  const handleDrop = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    const file = event.dataTransfer.files?.[0];
    if (file) {
      // Reset states
      setError(null);
      setProcessedImages(null);
      setSelectedFile(file);

      // Create a preview
      const reader = new FileReader();
      reader.onload = () => {
        setPreviewUrl(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleUploadClick = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  const handleProcess = async () => {
    if (!selectedFile) {
      setError('Please select an image first');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('image', selectedFile);

      const response = await fetch('http://localhost:5000/process-image', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to process image');
      }

      const data = await response.json();
      setProcessedImages(data);
    } catch (err) {
      setError((err as Error).message || 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 flex flex-col">
      {/* Navbar */}
      <nav className="bg-primary-dark text-white shadow-md">
        <div className="container mx-auto py-4 px-6 flex justify-between items-center">
          <div className="flex items-center">
            <svg
              className="h-8 w-8 mr-3"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
              />
            </svg>
            <h1 className="text-xl font-bold">Corner Detection Tool</h1>
          </div>
          <div className="flex space-x-4">
            <a href="#" className="hover:text-primary-100 transition duration-300">Home</a>
            <a href="#" className="hover:text-primary-100 transition duration-300">About</a>
            <a href="#" className="hover:text-primary-100 transition duration-300">Guide</a>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="flex-grow">
        <div className="container mx-auto px-4 py-8">
          <h1 className="text-3xl font-bold mb-8 text-center text-primary-300">
            Corner Detection Image Processor
          </h1>

          {/* Upload Section */}
          <div
            className="border-2 border-dashed border-primary-400 rounded-lg p-8 mb-8 text-center bg-primary-dark bg-opacity-30 "
            onDragOver={handleDragOver}
            onDrop={handleDrop}
          >
            <input
              type="file"
              ref={fileInputRef}
              className="hidden"
              accept="image/*"
              onChange={handleFileChange}
            />

            {previewUrl ? (
              <div className="mb-4">
                <img
                  src={previewUrl}
                  alt="Preview"
                  className="max-h-52 mx-auto rounded-lg transform scale-75"
                />
              </div>
            ) : (
              <div className="text-primary-200 mb-4">
                <svg
                  className="mx-auto h-16 w-16"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={1}
                    d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                  />
                </svg>
              </div>
            )}

            <button
              onClick={handleUploadClick}
              className="bg-primary cursor-pointer hover:bg-primary-light px-4 py-2 rounded-md mb-4 transition duration-300"
            >
              Select Image
            </button>

            <p className="text-primary-200 text-sm">
              or drag and drop your image here
            </p>
          </div>

          {/* Process Button */}
          <div className="flex justify-center mb-8">
            <button
              onClick={handleProcess}
              disabled={!selectedFile || isLoading}
              className={`px-6 py-3 rounded-md text-lg font-medium transition duration-300 ${!selectedFile || isLoading
                  ? 'bg-gray-600 cursor-not-allowed'
                  : 'bg-primary-500 hover:bg-primary-light'
                }`}
            >
              {isLoading ? 'Processing...' : 'Process Image'}
            </button>
          </div>

          {/* Error Message */}
          {error && (
            <div className="bg-red-900 text-red-100 p-4 rounded-md mb-8">
              {error}
            </div>
          )}

          {/* Results Section */}
          {processedImages && (
            <div className="bg-primary-dark bg-opacity-50 rounded-lg p-6 shadow-xl">
              <h2 className="text-2xl font-bold mb-6 text-center text-primary-100">
                Processing Results
              </h2>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <ImageCard title="Original Image" src={`data:image/jpeg;base64,${processedImages.original}`} />
                <ImageCard title="Grayscale" src={`data:image/jpeg;base64,${processedImages.grayscale}`} />
                <ImageCard title="Smoothed Image" src={`data:image/jpeg;base64,${processedImages.smooth}`} />
                <ImageCard title="Gradient Magnitude" src={`data:image/jpeg;base64,${processedImages.gradient}`} />
                <ImageCard title="Harris Response" src={`data:image/jpeg;base64,${processedImages.harris}`} />
                <ImageCard title="Gradient Angle" src={`data:image/jpeg;base64,${processedImages.angle}`} />
                <ImageCard title="Harris Corners" src={`data:image/jpeg;base64,${processedImages.harris_corners}`} />
                <ImageCard title="Good Features to Track" src={`data:image/jpeg;base64,${processedImages.gftt_corners}`} />
                <ImageCard title="Combined Corners" src={`data:image/jpeg;base64,${processedImages.combined_corners}`} />
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-primary-dark py-6 mt-8">
        <div className="container mx-auto px-6">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="mb-4 md:mb-0">
              <p className="text-primary-100">&copy; 2025 Corner Detection Tool</p>
            </div>
            <div className="flex space-x-4">
              <a href="#" className="text-primary-200 hover:text-white transition duration-300">Privacy</a>
              <a href="#" className="text-primary-200 hover:text-white transition duration-300">Terms</a>
              <a href="#" className="text-primary-200 hover:text-white transition duration-300">Contact</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

interface ImageCardProps {
  title: string;
  src: string;
}

function ImageCard({ title, src }: ImageCardProps) {
  return (
    <div className="bg-primary bg-opacity-20 rounded-lg overflow-hidden border border-primary-dark">
      <div className="p-3 bg-primary-dark border-b border-primary-dark">
        <h3 className="font-medium text-primary-100">{title}</h3>
      </div>
      <div className="p-2 flex justify-center">
        <img
          src={src}
          alt={title}
          className="w-full h-auto rounded transform scale-90"
        />
      </div>
    </div>
  );
}

export default App;