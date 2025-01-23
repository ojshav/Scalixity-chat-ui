import type React from "react"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"

const API_URL = "http://localhost:5000/api/chat"

export default function FAQ() {
  const [question, setQuestion] = useState("")
  const [answer, setAnswer] = useState("")
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ choice: "1", input: question }),
      })
      const data = await res.json()
      setAnswer(data.content)
    } catch (error) {
      console.error("Error:", error)
      setAnswer("An error occurred while fetching the answer.")
    }
    setIsLoading(false)
  }

  return (
    <div className="space-y-4">
      <form onSubmit={handleSubmit} className="space-y-4">
        <Input
          type="text"
          placeholder="Ask a question"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />
        <Button type="submit" disabled={isLoading || !question}>
          {isLoading ? "Loading..." : "Ask"}
        </Button>
      </form>
      {answer && <Textarea value={answer} readOnly className="h-40" />}
    </div>
  )
}

