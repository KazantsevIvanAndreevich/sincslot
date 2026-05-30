import AppRouter from "./routes/AppRouter.jsx";
import {ToastContainer} from "react-toastify";

function App() {
  return (
    <>
      <AppRouter/>
      <ToastContainer
        position="top-right"
        autoClose={5000}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
      />
    </>
  );
}

export default App;
