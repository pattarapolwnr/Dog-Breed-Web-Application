// import './App.css';
// import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
// import { faCloudArrowUp } from '@fortawesome/free-solid-svg-icons';

import { Link } from 'react-router-dom';

function Snapchat() {
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
            {/* <Link
              to="/"
              className="md:ml-20 font-lgt text-base text-textPrimary text-center"
            >
              Back to Input Image page
            </Link> */}
          </div>

          <div className="flex flex-col md:flex-row justify-center items-center my-10 space-y-8 md:space-y-0 md:my-10 md:space-x-20">
            {/* Image Preview Section */}
            <div className="flex flex-col justify-center space-y-4">
              <img src={'http://localhost:5000/video_feed'} width={300} />
              <h5 className="font-lgt text-base text-textPrimary text-center">
                Live Webcam Preview
              </h5>
            </div>

            {/* Right Section */}
            <div className="flex flex-col justify-center space-y-10">
              <Link to={'/'}>
                <div className="flex justify-center items-center">
                  <h5 className="text-center bg-secondary rounded-xl w-48 px-1 py-2 border-2 border-white text-white transition ease-in-out delay-75 hover:border-secondary hover:text-secondary hover:bg-white">
                    Back to input image
                  </h5>
                </div>
              </Link>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default Snapchat;
