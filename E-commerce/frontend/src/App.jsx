import {BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ProductDetails from './pages/ProductDetails';
import ProductList from './pages/Product_list';
import Navbar from './components/Navbar';
import CartPage from './pages/CartPage';

function App() {
  

  return (
    <div className="pt-20">
      <Router>
        <Navbar />
        <Routes>
          <Route path="/" element={<ProductList />} />
          <Route path="/product/:id" element={<ProductDetails />} />
          <Route path="/cart" element={<CartPage />} />
        </Routes>
      </Router>
    </div>
    
  )
}

export default App
