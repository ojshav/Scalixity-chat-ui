import type React from "react"
import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Textarea } from "@/components/ui/textarea"

const API_URL = "http://localhost:5000/api/chat"

export default function ShoppingAssistant() {
  const [categories, setCategories] = useState<string[]>([])
  const [sizes, setSizes] = useState<string[]>([])
  const [colors, setColors] = useState<string[]>([])
  const [selectedCategory, setSelectedCategory] = useState("")
  const [selectedSize, setSelectedSize] = useState("")
  const [selectedColor, setSelectedColor] = useState("")
  const [response, setResponse] = useState("")
  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    fetchCategories()
  }, [])

  useEffect(() => {
    if (selectedCategory) {
      fetchSizes(selectedCategory)
    }
  }, [selectedCategory])

  useEffect(() => {
    if (selectedCategory && selectedSize) {
      fetchColors(selectedCategory, selectedSize)
    }
  }, [selectedCategory, selectedSize])

  const fetchCategories = async () => {
    try {
      const res = await fetch(`${API_URL}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ choice: "2", input: "get_categories" }),
      })
      const data = await res.json()
      setCategories(data.content)
    } catch (error) {
      console.error("Error fetching categories:", error)
    }
  }

  const fetchSizes = async (category: string) => {
    try {
      const res = await fetch(`${API_URL}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ choice: "2", input: `get_sizes ${category}` }),
      })
      const data = await res.json()
      setSizes(data.content)
    } catch (error) {
      console.error("Error fetching sizes:", error)
    }
  }

  const fetchColors = async (category: string, size: string) => {
    try {
      const res = await fetch(`${API_URL}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ choice: "2", input: `get_colors ${category} ${size}` }),
      })
      const data = await res.json()
      setColors(data.content)
    } catch (error) {
      console.error("Error fetching colors:", error)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          choice: "2",
          input: `find_products ${selectedCategory} ${selectedSize} ${selectedColor}`,
        }),
      })
      const data = await res.json()
      
      // Format the response for better readability
      const formattedResponse = data.content.map((product: any) => 
        `Product: ${product.name}\n` +
        `Company: ${product.company}\n` +
        `Recommendation: ${product.recommendation}\n` 
      ).join('');
  
      setResponse(formattedResponse)
    } catch (error) {
      console.error("Error:", error)
      setResponse("An error occurred while fetching product recommendations.")
    }
    setIsLoading(false)
  }
  return (
    <div className="space-y-4">
      <form onSubmit={handleSubmit} className="space-y-4">
        <Select onValueChange={setSelectedCategory}>
          <SelectTrigger>
            <SelectValue placeholder="Select a category" />
          </SelectTrigger>
          <SelectContent>
            {categories.map((category) => (
              <SelectItem key={category} value={category}>
                {category}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
        {selectedCategory && (
          <Select onValueChange={setSelectedSize}>
            <SelectTrigger>
              <SelectValue placeholder="Select a size" />
            </SelectTrigger>
            <SelectContent>
              {sizes.map((size) => (
                <SelectItem key={size} value={size}>
                  {size}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        )}
        {selectedSize && (
          <Select onValueChange={setSelectedColor}>
            <SelectTrigger>
              <SelectValue placeholder="Select a color" />
            </SelectTrigger>
            <SelectContent>
              {colors.map((color) => (
                <SelectItem key={color} value={color}>
                  {color}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        )}
        <Button type="submit" disabled={isLoading || !selectedCategory || !selectedSize || !selectedColor}>
          {isLoading ? "Loading..." : "Find Products"}
        </Button>
      </form>
      {response && <Textarea value={response} readOnly className="h-40" />}
    </div>
  )
}

