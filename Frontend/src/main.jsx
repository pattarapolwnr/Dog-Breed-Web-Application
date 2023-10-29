import React from 'react';
import ReactDOM from 'react-dom/client';
import Root from './routes/root';
import './index.css';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import Snapchat from './routes/snapchat';

const router = createBrowserRouter([
  {
    path: '/',
    element: <Root />,
  },
  {
    path: '/live_webcam',
    element: <Snapchat />,
  },
]);

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);
