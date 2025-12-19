import React, { useState } from 'react';
import { useState } from 'react';
import { Search, ShoppingCart, User, Heart, Filter, Star } from 'lucide-react';
import { Product } from '../App';
import { ImageWithFallback } from './figma/ImageWithFallback';
import { getData, deleteData{data_id}, createData, createNotifications, logout, updateData{data_id}, getDashboard, login, createLogin, createRegister } from './services/api';
const MOCK_PRODUCTS: Product[] = [];
const [CATEGORIES, setCATEGORIES] = useState([]);
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const data = await getItems();
        setData(data);
        setError(null);
      } catch (error) {
        console.error('Error fetching data:', error);
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };
    
    fetchData();
  }, []);

interface HomePageProps {
  onProductClick: (product: Product) => void;
  onNavigateToCart: () => void;
  onNavigateToAccount: () => void;
  cartItemCount: number;
}
export function HomePage({ onProductClick, onNavigateToCart, onNavigateToAccount, cartItemCount }: HomePageProps) {null});
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="sticky top-0 z-50 bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between gap-4">
            <h1 className="text-white bg-gradient-to-r from-[#5743E9] to-[#5251D7] px-6 py-2 rounded-lg shadow-lg" 
                style={{ textShadow: '0 2px 4px rgba(0,0,0,0.2)' }}>
              TechStore
            </h1>
            <div className="flex-1 max-w-2xl">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input
                  type="text"
                  placeholder="Search products..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#5743E9]"
                />
              </div>
            </div>
            <div className="flex items-center gap-3">
              <button
                onClick={onNavigateToCart}
                className="relative p-2 bg-[#5743E9] text-white rounded-lg hover:bg-[#6853f0] transition-all duration-300"
              >
                <ShoppingCart className="w-5 h-5" />
                {cartItemCount > 0 && (
                  <span className="absolute -top-1 -right-1 bg-[#4DDAD9] text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                    {cartItemCount}
                  </span>
                )}
              </button>
              <button
                onClick={onNavigateToAccount}
                className="p-2 bg-[#5743E9] text-white rounded-lg hover:bg-[#6853f0] transition-all duration-300"
              >
                <User className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      </header>
      {/* Hero Banner */}
      <div 
        className="bg-gradient-to-r from-[#5743E9] to-[#5251D7] text-white py-16 px-4"
        style={{ textShadow: '0 2px 8px rgba(0,0,0,0.3)' }}
      >
        <div className="max-w-7xl mx-auto text-center">
          <h2 className="text-white mb-4">Welcome to Your Premium Tech Store</h2>
          <p className="text-white text-xl mb-6">Discover the latest electronics with unbeatable prices</p>
          <div className="flex justify-center gap-4">
            <button className="bg-[#4DDAD9] text-white px-8 py-3 rounded-lg hover:opacity-90 transition-all duration-300">
              Shop Now
            </button>
            <button className="bg-white/20 text-white px-8 py-3 rounded-lg hover:bg-white/30 transition-all duration-300 backdrop-blur-sm">
              View Deals
            </button>
          </div>
        </div>
      </div>
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Category Filters */}
        <div className="mb-8">
          <div className="bg-[#5743E9] text-white px-6 py-3 rounded-t-lg">
            <h3 className="text-white">Browse by Category</h3>
          </div>
          <div className="flex flex-wrap gap-3 bg-white p-6 rounded-b-lg shadow-md">
            {CATEGORIES.map(category => (
              <button
                key={category}
                onClick={() => setSelectedCategory(category)}
                className={`px-6 py-2 rounded-lg transition-all duration-300 ${
                  selectedCategory === category
                    ? 'bg-[#4DDAD9] text-white shadow-lg'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {category}
              </button>
            ))}
          </div>
        </div>
        {/* Price Filter */}
        <div className="mb-8 flex items-center gap-4">
          <div className="flex items-center gap-2">
            <Filter className="w-5 h-5 text-[#5743E9]" />
            <span className="text-gray-700">Price Range:</span>
          </div>
          <div className="flex gap-2">
            {[
              { value: 'all', label: 'All Prices' },
              { value: 'low', label: 'Under $300' },
              { value: 'mid', label: '$300 - $700' },
              { value: 'high', label: 'Over $700' },
            ].map(filter => (
              <button
                key={filter.value}
                onClick={() => setPriceFilter(filter.value as any)}
                className={`px-4 py-2 rounded-lg transition-all duration-300 ${
                  priceFilter === filter.value
                    ? 'bg-[#4DDAD9] text-white'
                    : 'bg-white text-gray-700 border border-gray-300 hover:border-[#5743E9]'
                }`}
              >
                {filter.label}
              </button>
            ))}
          </div>
        </div>
        {/* Product Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredProducts.map(product => (
            <div
              key={product.id}
              onClick={() => onProductClick(product)}
              className="bg-white rounded-lg overflow-hidden cursor-pointer transition-all duration-300 hover:scale-105"
              style={{ boxShadow: `0 4px 12px rgba(87, 67, 233, 0.15)` }}
            >
              <div className="relative aspect-square overflow-hidden">
                <ImageWithFallback
                  src={product.image}
                  alt={product.name}
                  className="w-full h-full object-cover"
                />
                {product.stock < 50 && (
                  <div className="absolute top-3 right-3 bg-gradient-to-r from-[#5251D7] to-[#4DDAD9] text-white px-3 py-1 rounded-full text-sm">
                    Low Stock
                  </div>
                )}
              </div>
              <div className="p-4">
                <div className="flex items-start justify-between mb-2">
                  <h3 className="text-gray-900 flex-1">{product.name}</h3>
                  <Heart className="w-5 h-5 text-gray-400 hover:text-red-500 transition-colors flex-shrink-0 ml-2" />
                </div>
                <p className="text-gray-600 text-sm mb-3 line-clamp-2">{product.description}</p>
                <div className="flex items-center gap-2 mb-3">
                  <div className="flex items-center gap-1">
                    <Star className="w-4 h-4 fill-[#4DDAD9] text-[#4DDAD9]" />
                    <span className="text-sm text-gray-700">{product.rating}</span>
                  </div>
                  <span className="text-sm text-gray-500">({product.reviews} reviews)</span>
                </div>
                <div className="flex items-center justify-between">
                  <div>
                    <div className="text-gray-900">${product.price.toFixed(2)}</div>
                    <div className="text-sm text-gray-500">{product.stock} in stock</div>
                  </div>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      onProductClick(product);
                    }}
                    className="bg-[#5743E9] text-white px-4 py-2 rounded-lg hover:bg-[#6853f0] transition-all duration-300"
                  >
                    View Details
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
        {filteredProducts.length === 0 && (
          <div className="text-center py-16">
            <p className="text-gray-500 text-xl">No products found matching your criteria</p>
          </div>
        )}
      </div>
    </div>
  );
}
