import { useEffect,useState } from "react";
import ProductCard from "../components/ProductCard";


function ProductList() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const BASE_URL=import.meta.env.VITE_DJANGO_BASE_URL;

  useEffect(() => {
    async function fetchProducts() {
      try {
        const response = await fetch(`${BASE_URL}/api/product/`);
        if (!response.ok) {
          throw new Error('Failed to load products');
        }
        const data = await response.json();
        setProducts(data);
      } catch (error) {
        setError(error);
      } finally {
        setLoading(false);
      }
    }

    fetchProducts();
  }, [BASE_URL]);

  if(loading){
    return <div className="text-center ">Loading...</div>;
  }

  if(error){
    return <div className="text-center text-red-500">Error: {error.message}</div>;
  }

  return (
    <div className="min-h-screen bg-gray-100 p-4">
        {/* top corner */}
      <h1 className=" text-3xl font-bold text-center py-6 px-6 bg-white shadow flex mb-4 ">Product List</h1> 
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      {products.length === 0 ? (
        <div className="text-center col-span-full">No products available.</div>
      ) : (
        products.map((product) => (
          <ProductCard key={product.id} product={product} />
        ))
      )}
      </div>
    </div>
  );
}
export default ProductList;