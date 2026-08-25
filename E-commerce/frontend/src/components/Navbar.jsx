import { Link, useNavigate } from "react-router-dom";
import { useCart } from "../context/useCart";
import { clearToken, getAccessToken } from "../utils/auth";

function Navbar() {
  const { cartItems } = useCart();
  const navigate = useNavigate();
  const isLoggedIn = !!getAccessToken();
  const handleLogout = () => {
    clearToken();
    navigate("/login");
  };
  const cartCount = cartItems.reduce((total, item) => total + item.quantity, 0);
  return (
    <nav className="bg-white shadow-md px-6 py-4 flex justify-between items-center fixed w-full top-0 z-50">
      <Link to="/" className="text-2xl font-bold text-grey-800">
        My Store
      </Link>
      <div className="flex items-center space-x-4 gap-4">
        {isLoggedIn ? (
          <button
            onClick={handleLogout}
            className="text-grey-800 hover:text-grey-600 font-medium "
          >
            Logout
          </button>
        ) : (
          <div>
            <Link
              to="/login"
              className="text-grey-800 hover:text-grey-600 font-medium m-4"
            >
              Login
            </Link>
            <Link
              to="/register"
              className="text-grey-800 hover:text-grey-600 font-medium m-4"
            >
              Register
            </Link>
          </div>
        )}
      </div>
      <Link
        to="/cart"
        className="relative  text-grey-800 hover:text-grey-600 font-medium"
      >
        Cart (
        {cartCount > 0 && (
          <span className="absolute -top-2 -right-2 bg-red-600 text-white text-xs font-bold rounded-full h-5 w-5 flex items-center justify-center px-2 py-1">
            {cartCount}
          </span>
        )}
        )
      </Link>
    </nav>
  );
}
export default Navbar;
