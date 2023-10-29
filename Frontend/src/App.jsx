import './App.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCloudArrowUp } from '@fortawesome/free-solid-svg-icons';
import { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [selectedFile, setSelectedFile] = useState();
  const [preview, setPreview] = useState();
  const [data, setData] = useState('');
  const [val, setVal] = useState('Upload image to predict');
  const [isLoading, setIsLoading] = useState(false);

  const [filename, setFilename] = useState('No file Uploaded');

  useEffect(() => {
    fetch('http://localhost:5000')
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        setData(data.message);
      });
  }, [data]);
  const [file, setFile] = useState(null);

  const handleSubmit = async (event) => {
    event.preventDefault();

    const formData = new FormData();
    formData.append('file', file);

    try {
      setIsLoading(true);
      const res = await axios.post('http://localhost:5000/upload', formData);
      const data = await res.data.message;
      setVal(data);
      setIsLoading(false);
      // axios.post('http://localhost:5000/upload', formData).then((res) => {
      //   console.log(res.data.message);
      //   setVal(res.data.message);
      // });
      alert('File uploaded successfully');
    } catch (error) {
      console.error(error);
    }
  };
  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    setSelectedFile(file);
    setFilename(file.name);
  };

  useEffect(() => {
    if (!selectedFile) {
      setPreview(undefined);
      return;
    }
    // create the preview
    const objectUrl = URL.createObjectURL(selectedFile);
    setPreview(objectUrl);

    // free memory when ever this component is unmounted
    return () => URL.revokeObjectURL(objectUrl);
  }, [selectedFile]);
  return (
    <>
      <div className="flex items-center justify-center min-h-screen">
        {/* Card container */}
        <div className="relative flex flex-col m-6 shadow-2xl rounded-2xl bg-white  px-6 py-6 w-11/12 md:w-4/5 xl:w-3/5">
          {/* Title */}
          <div className="flex flex-col md:flex-row justify-start items-center">
            <img src="/images/siit_logo.png" className="lg:mr-32" />
            <h1 className="font-sbld text-3xl text-center text-transparent h-20 md:h-12 bg-clip-text bg-gradient-to-r from-purple-400 to-pink-600 ">
              Dog Bleed Classification
            </h1>
          </div>

          <div className="flex flex-col md:flex-row justify-center items-center my-10 space-y-8 md:space-y-0 md:my-10 md:space-x-20">
            {/* Image Preview Section */}
            <div className="flex flex-col justify-center space-y-4">
              <img src={preview} width={300} />
              <h5 className="font-lgt text-base text-textPrimary text-center">
                Input Image Preview
              </h5>
            </div>

            {/* Right Section */}
            <div className="flex flex-col justify-center space-y-10">
              <form></form>
              <label
                htmlFor="upload-photo"
                className="bg-bgFile border-dashed border-2 border-bgBorderFile cursor-pointer rounded-xl lg:w-96 h-36"
              >
                <div className="flex flex-col justify-center items-center py-7 space-y-2">
                  <FontAwesomeIcon
                    icon={faCloudArrowUp}
                    style={{ fontSize: '48px', color: '#8B2CF5' }}
                  />
                  <h1 className="text-base font-med text-textPrimary">
                    SELECT A FILE
                  </h1>
                  <h1 className="text-sm font-reg text-gray-400">
                    File name: {filename}
                  </h1>
                </div>
              </label>
              <input
                type="file"
                name="photo"
                id="upload-photo"
                className="hidden"
                onChange={(e) => {
                  setFile(e.target.files[0]);
                  handleFileUpload(e);
                }}
              />
              <div className="flex justify-center items-center">
                <button
                  className="bg-secondary rounded-xl w-48 px-1 py-2 border-2 border-white text-white transition ease-in-out delay-75 hover:border-secondary hover:text-secondary hover:bg-white"
                  type="submit"
                  onClick={handleSubmit}
                >
                  Predict
                </button>
              </div>

              {/* Prediction Text */}

              {/* Hello, human! You look like a Cavalier_king_charles_spaniel. */}
              {isLoading ? (
                <div className="flex justify-center items-center">
                  <div
                    className="inline-block h-8 w-8 animate-spin rounded-full border-primary border-4 border-solid border-current border-r-transparent align-[-0.125em] motion-reduce:animate-[spin_1.5s_linear_infinite]"
                    role="status"
                  >
                    <span className="!absolute !-m-px !h-px !w-px !overflow-hidden !whitespace-nowrap !border-0 !p-0 ![clip:rect(0,0,0,0)]">
                      Loading...
                    </span>
                  </div>
                </div>
              ) : (
                <h3 className="font-reg text-2xl max-w-sm text-center text-textSecondary">
                  {val}{' '}
                </h3>
              )}
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default App;
