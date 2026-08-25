import { Link } from 'react-router-dom';
import {useCart} from '../context/useCart';
function CartPage(){
    const BASEURL=import.meta.env.VITE_DJANGO_BASE_URL;
    const {cartItems,removeFromCart,updateQuantity}=useCart();
    const totalPrice=cartItems.reduce(
        (total,item)=>total+Number(item.product_price)*Number(item.quantity),
        0
    );

    return(
        <div className="min-h-screen bg-gray-100 py-10">
            <div className="max-w-6xl mx-auto bg-white shadow-md rounded-lg p-6">
                <h1 className="text-3xl font-bold mb-6">Shopping Cart</h1>
                <div className="space-y-4">
                    {cartItems.length === 0 ? (
                        <p>Your cart is empty.</p>
                    ):(
                        cartItems.map((item) => (
                            <div key={item.id} className="flex items-center justify-between border-b pb-4">
                                <div className="flex items-center">
                                    <img src={`${BASEURL}${item.product_image}`} alt={item.product_name} className="w-16 h-16 object-cover rounded-md" />
                                    <div className="ml-4">
                                        <h2 className="text-lg font-semibold">{item.product_name}</h2>
                                        <p className="text-gray-600">Price: {item.product_price} Tk</p>
                                    </div>
                                </div>
                                <div className="flex items-center">
                                    <button onClick={() => updateQuantity(item.id, item.quantity - 1)} className="bg-gray-300 text-gray-700 py-1 px-3 rounded-l hover:bg-gray-400">
                                        -
                                    </button>
                                    <span className="bg-gray-200 text-gray-700 py-1 px-3">{item.quantity}</span>
                                    <button onClick={() => updateQuantity(item.id, item.quantity + 1)} className="bg-gray-300 text-gray-700 py-1 px-3 rounded-r hover:bg-gray-400">
                                        +
                                    </button>
                                    <button onClick={() => removeFromCart(item.id)} className="ml-4 bg-red-500 text-white py-1 px-3 rounded hover:bg-red-600">
                                        Remove
                                    </button>
                                </div>
                            </div>
                        ))
                    )}
                </div>
                <div className="mt-6 flex justify-between items-center">
                    <p className="text-xl font-bold">Total: {totalPrice} Tk</p>
                    {/* <button className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600">
                        Checkout
                    </button> */}
                    <Link to="/checkout" className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600">
                        Proceed to Checkout
                    </Link>
                </div>
            </div>
        </div>
    );
}
export default CartPage;