import React, { useState } from "react"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import FAQ from "./components/FAQ"
import ShoppingAssistant from "./components/ShoppingAssistant"

export default function App() {
  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
      <Card className="w-full max-w-4xl">
        <CardHeader>
          <CardTitle>Scalixity Assistant</CardTitle>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="faq">
            <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger value="faq">FAQ</TabsTrigger>
              <TabsTrigger value="shopping">Shopping Assistant</TabsTrigger>
            </TabsList>
            <TabsContent value="faq">
              <FAQ />
            </TabsContent>
            <TabsContent value="shopping">
              <ShoppingAssistant />
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
    </div>
  )
}

