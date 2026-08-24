import { createContext,useContext,useState,useEffect } from "react";

const CartContext=createContext();
export const CartProvider=({children})=>{
    const BASE_URL=import.meta.env.VITE_DJANGO_BASE_URL;
    const [cartItems,setCartItems]=useState([])
    const[total,setTotal]=useState(0);

    useEffect(()=>{
        const fetchCart=async()=>{
            try{
                const response=await fetch(`${BASE_URL}/api/cart/`);
                if (!response.ok){
                    throw new Error("Failed to fetch cart");
                }
                const data=await response.json();
                setCartItems(data.items);
                setTotal(data.total);
            }catch(error){
                console.error("Error fetching cart:",error);
            }
        };
        fetchCart();
    },[BASE_URL]);

//Add product to 

const addToCart=async(product)=>{
    // const existing=cartItems.find((item)=>item.id===product.id)
    // if (existing){
    //     setCartItems(
    //         cartItems.map((item)=>(
    //             item.id===product.id ?{...item,quantity:item.quantity+1}:item

    //         )
    //     )
    //     )
    // }else{
    //     setCartItems([...cartItems,{...product,quantity:1}]);
    // }

    // Send a POST request to the backend to add the product to the cart
    try {
        const response = await fetch(`${BASE_URL}/api/cart/add/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ product_id: product.id, quantity: 1 }),
        });

        if (!response.ok) {
            throw new Error("Failed to add product to cart");
        }

        const data = await response.json();
        setCartItems(data.cart.items);
        setTotal(data.cart.total);
    } catch (error) {
        console.error("Error adding product to cart:", error);
    }

};
//remove product
// const removeFromCart=(id)=>{
//     setCartItems(cartItems.filter((item)=>item.id!==id))
// };

const removeFromCart=async(id)=>{
    try {
        const response = await fetch(`${BASE_URL}/api/cart/remove/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ item_id: id }),
        });

        if (!response.ok) {
            throw new Error("Failed to remove product from cart");
        }

        const data = await response.json();
        setCartItems(data.cart.items);
        setTotal(data.cart.total);
    } catch (error) {
        console.error("Error removing product from cart:", error);
    }
};  

// const updateQuantity=(id,quantity)=>{
//     if (quantity<1) return;
//     setCartItems(
//         cartItems.map((item)=> item.id==id ?{...item,quantity}:item)
//     )
// }

const updateQuantity=async(id,quantity)=>{
    if (quantity < 1) return;
    try {
        const response = await fetch(`${BASE_URL}/api/cart/update/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ item_id: id, quantity: quantity }),
        });

        if (!response.ok) {
            throw new Error("Failed to update cart quantity");
        }

        const data = await response.json();
        setCartItems(data.cart.items);
        setTotal(data.cart.total);
    } catch (error) {
        console.error("Error updating cart quantity:", error);
    }
};

return(
    // <CartContext.Provider
    // value={{cartItems,addToCart,removeFromCart,updateQuantity
    // }}>
    //      {children} 
    // </CartContext.Provider>
    <CartContext.Provider value={{cartItems,addToCart,removeFromCart,updateQuantity,total}}>
        {children}
    </CartContext.Provider>
);


};
export const useCart=()=>useContext(CartContext);