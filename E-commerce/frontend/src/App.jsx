import { useEffect, useState } from 'react'
import ProductList from '../pages/Product_list'
import {BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ProductDetails from '../pages/ProductDetails'
function App() {
  

  return (
    <div>
      <Router>
        <Routes>
          <Route path="/" element={<ProductList />} />
          <Route path="/product/:id" element={<ProductDetails />} />
        </Routes>
      </Router>
    </div>
    
  )
}

export default App
