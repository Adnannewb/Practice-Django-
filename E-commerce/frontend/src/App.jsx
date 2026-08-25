import {BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ProductDetails from './pages/ProductDetails';
import ProductList from './pages/Product_list';
import Navbar from './components/Navbar';
import CartPage from './pages/CartPage';
import CheckoutPage from './pages/CheckoutPage';
import SignUp from './pages/SignUp';
import Login from './pages/Login';
import PrivateRouter from './components/PrivateRouter';

function App() {
  

  return (
    <div className="pt-20">
      <Router>
        <Navbar />
        <Routes>
          <Route path="/" element={<ProductList />} />
          <Route path="/product/:id" element={<ProductDetails />} />
          <Route path="/cart" element={<CartPage />} />
          <Route element={<PrivateRouter />}>
            <Route path="/checkout" element={<CheckoutPage />} />
          </Route>
          <Route path="/register" element={<SignUp />} />
          <Route path="/login" element={<Login />} />
          
        </Routes>
      </Router>
    </div>
    
  )
}

export default App
