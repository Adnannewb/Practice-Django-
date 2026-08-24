import {Link} from 'react-router-dom';
import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom';
import { useCart } from '../context/CartContext';

function ProductDetails() {
    const BASE_URL=import.meta.env.VITE_DJANGO_BASE_URL;
    const { id } = useParams();
    const [product, setProduct] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const { addToCart } = useCart();

    useEffect(() => {
        async function fetchProduct() {
            try {   
                const response = await fetch(`${BASE_URL}/api/product/${id}/`);
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                setProduct(data);
            } catch (error) {
                setError(error.message);
            } finally {
                setLoading(false);
            }
        }

        fetchProduct();
    }, [id,BASE_URL]);

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error}</div>;
    if (!product) return <div>Product not found</div>;

  return (
    <div>
      
      {/* Add your product details content here */}
        <div className="min-h-screen bg-gray-100 py-10">
        <div className="max-w-6xl mx-auto bg-white shadow-md rounded-lg p-6 flex flex-col md:flex-row gap-6">
            <div className="md:w-1/2">
                <img src={`${product.image}`} alt={product.name} className="w-full h-auto object-fit rounded-lg" />
            </div>
            <div className="md:w-1/2 flex flex-col justify-between">
                <div>
                    <h1 className="text-3xl font-bold mb-4">{product.name}</h1>
                    <p className="text-gray-700 mb-4">{product.description}</p>
                    <p className="text-2xl font-bold mb-4">{product.price} Tk</p>
                </div>
                <div className="flex flex-col gap-4">
                    <Link to="/" className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 text-center">Back to Product List</Link>
                    <button onClick={() => addToCart(product)} className="bg-green-500 text-white py-2 px-4 rounded hover:bg-green-600">Add to Cart</button>
                </div>
            </div>
        </div>
    </div>
      </div>
    );
}
export default ProductDetails;