import { useState } from "react"

const API_URL = "http://localhost:5000/api/chat"

export function useChat() {
  const [choice, setChoice] = useState<string>("")
  const [input, setInput] = useState<string>("")
  const [response, setResponse] = useState<string>("")
  const [isLoading, setIsLoading] = useState<boolean>(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ choice, input }),
      })
      const data = await res.json()
      setResponse(JSON.stringify(data.content, null, 2))
    } catch (error) {
      console.error("Error:", error)
      setResponse("An error occurred while fetching the response.")
    }
    setIsLoading(false)
  }

  return {
    choice,
    setChoice,
    input,
    setInput,
    response,
    isLoading,
    handleSubmit,
  }
}

