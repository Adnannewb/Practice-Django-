import {useState} from "react";
import {useNavigate} from "react-router-dom";
import {useCart} from "../context/useCart";
import {authFetch} from "../utils/auth";

function CheckoutPage() {
    const BASEURL=import.meta.env.VITE_DJANGO_BASE_URL;
    const navigate = useNavigate();
    const {clearCart} = useCart();

    const [form,setForm]=useState({
        name:"",
        address:"",
        phone:"",
        payment_method:"COD",
    });
    const [loading,setLoading]=useState(false);
    const [message,setMessage]=useState(null);

    const handleChange=(e)=>{
        setForm({
            ...form,
            [e.target.name]:e.target.value,
        });
    }
    const handleSubmit=async(e)=>{
        e.preventDefault();
        setLoading(true);
        try{
            const response=await authFetch(`${BASEURL}/api/orders/create/`,{
                method:"POST",
                headers:{
                    "Content-Type":"application/json",
                },
                body:JSON.stringify(form),
            });
            const data=await response.json();
            if(response.ok){
                setMessage("Order placed successfully!");
                clearCart();
                setTimeout(()=>{
                    navigate("/");
                },3000);
            }else{
                setMessage(data.error || "Failed to place order.");
            }
        }catch(error){
            console.error("Error placing order:", error);
            setMessage("An error occurred while placing the order.");
        }finally{
            setLoading(false);
        }
    };
    return (
        <div className="min-h-screen bg-gray-100 flex items-center justify-center p-6">
            <div className="bg-white p-8 rounded shadow-md w-full max-w-md">
                <h2 className="text-2xl font-bold mb-6">Checkout</h2>
                <form onSubmit={handleSubmit} className="space-y-4">
                    <input
                        type="text"
                        name="name"
                        placeholder="Full Name"
                        value={form.name}
                        onChange={handleChange}
                        className="w-full p-2 border border-gray-300 rounded"   
                        />
                    <textarea
                        name="address"
                        placeholder="Address"
                        value={form.address}
                        onChange={handleChange}
                        className="w-full p-2 border border-gray-300 rounded"
                    />
                    <input
                        type="text"
                        name="phone"
                        placeholder="Phone Number"
                        value={form.phone}
                        onChange={handleChange}
                        className="w-full p-2 border border-gray-300 rounded"
                    />
                    <select
                        name="payment_method"
                        value={form.payment_method}
                        onChange={handleChange}
                        className="w-full p-2 border border-gray-300 rounded"
                    >
                        <option value="COD">Cash on Delivery</option>
                        <option value="Online Payment">Online Payment</option>
                        <option value="Credit Card">Credit Card</option>
                    </select>
                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600 transition duration-300"
                    >
                        {loading ? "Placing Order..." : "Place Order"}
                    </button>
                    {message && <p className="mt-4 text-center text-green-500">{message}</p>}
                </form>
            </div>
        </div>
    );
}

export default CheckoutPage;
