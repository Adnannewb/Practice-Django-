import { Link } from "react-router-dom";

function ProductCard({ product }) {
    const BASE_URL=import.meta.env.VITE_DJANGO_BASE_URL;
  return (
    <div className="bg-white shadow-md rounded-lg p-4 m-4">
      <img src={`${BASE_URL}${product.image}`} alt={product.name} className="w-full h-48 object-cover mb-4" />
      <h2 className="text-xl font-bold">{product.name}</h2>
      {/* <p className="text-gray-600">{product.description}</p> */}
      <p className="text-2xl font-bold">{product.price} Tk</p>
      <Link to={`/product/${product.id}`} className="text-blue-500 hover:underline mt-2 inline-block cursor-pointer">
        View Details
      </Link>

    </div>
  );
}
export default ProductCard;