import React, { useState, useEffect } from "react";
import { Container, Text, ScrollView, View, VStack, Box, Spinner, HStack } from "native-base";
import Header from "./Header";
import * as styles from "@styles/index";
import ButtonArea from "./ButtonArea";
import Triangle from "./components/Triangle";

interface IMessage {
  id: number;
  content: string;
  isUserMessage?: boolean;
}
const LoadingBox = () => (
  <HStack bg={"#fff"} borderRadius={5} w={'35%'} p={2} px={3} space={3} position="relative">
    <Spinner  color="primary.500" />
    <Text color="primary.500">查詢中...</Text>
    <Triangle type={"server"} />
  </HStack>
);

const ChatApp: React.FC = () => {
  const [messages, setMessages] = useState<IMessage[]>([]);
  const [userMessage, setUserMessage] = useState<IMessage[]>([]);
  const [inputMessage, setInputMessage] = useState<string>("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    console.log("change", messages);
    let target = messages[messages.length - 1];
    fetchData(target); // 初始化加载一次数据
  }, [userMessage]);

  const fetchData = async (target: IMessage) => {
    setLoading(true);
    try {
      console.log("Fetching data...", target);
      // 向后端发送消息
      const response = await fetch("http://127.0.0.1:5000/send-message", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: target.content }),
      });
      if (!response.ok) {
        throw new Error("Failed to send message");
      } else {
        const data = await response.json();
        console.log("!!!!!!!!!!!!!!!!", data);
        const entityMessages = data.entities.map((entity: any) => `${entity[0]}: ${entity[1]}`);
        const NERMessage: IMessage = {
          id: messages.length,
          content: '{\n' + entityMessages.join("\n") + '\n}',
          isUserMessage: false,
        };
        // setMessages([...messages, NERMessage]);
        const newMessage: IMessage = {
          id: messages.length,
          content: data.message,
          isUserMessage: false,
        };

        const newMessage2: IMessage = {
          id: messages.length,
          content: data.ano,
          isUserMessage: false,
        };
        setMessages([...messages, NERMessage, newMessage, newMessage2]);
      }
    } catch (error) {
      console.error("Error:", error);
    }
    setLoading(false);
  };

  const pushUserMsg = () => {
    const newMessage: IMessage = {
      id: messages.length,
      content: inputMessage,
      isUserMessage: true,
    };
    setMessages([...messages, newMessage]);
    setUserMessage([...messages, newMessage]);
  };

  const sendMessage = async () => {
    await pushUserMsg();
    setInputMessage(""); // 清空输入框
  };

  return (
    <Container flex={1} {...styles.wh100} w={"100%"}>
      <Header />
      <View flex={5} w={"100%"}>
        <ScrollView
          flex={1}
          bg={"#54cffd54"}
          w={"100%"}
          {...styles.topBorder}
          py={10}
          px={5}
        >
          <VStack space={3} w={"100%"}>
            {messages.map((message) => (
              <Box
                key={message.id}
                bg={message.isUserMessage ? "#5FD3FF" : "#fff"}
                borderRadius={5}
                p={2}
                ml={message.isUserMessage ? "auto" : 0}
                mr={!message.isUserMessage ? "auto" : 0}
                position="relative"
              >
                <Text fontSize={"lg"}>{message.content}</Text>
                <Triangle type={message.isUserMessage ? "user" : "server"} />
              </Box>
            ))}
            {loading ? <LoadingBox /> : <Text></Text>}
          </VStack>
        </ScrollView>
      </View>

      <ButtonArea
        sendMessage={sendMessage}
        inputMessage={inputMessage}
        setInputMessage={setInputMessage}
      />
    </Container>
  );
};

export default ChatApp;
