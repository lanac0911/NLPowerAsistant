import React, { useState, useEffect } from "react";
import {
  Container,
  Text,
  ScrollView,
  View,
  VStack,
  Box,
  Spinner,
  HStack,
  WarningTwoIcon,
  SunIcon,
} from "native-base";
import Header from "./Header";
import * as styles from "@styles/index";
import ButtonArea from "./ButtonArea";
import Triangle from "./components/Triangle";

interface IMessage {
  id: number;
  content: string;
  isUserMessage?: boolean;
  color?: string;
  type?: string;
  randomApp?: string
}
const LoadingBox = () => (
  <HStack
    bg={"#fff"}
    borderRadius={5}
    w={"35%"}
    p={2}
    px={3}
    space={3}
    position="relative"
  >
    <Spinner color="primary.500" />
    <Text color="primary.500">查詢中...</Text>
    <Triangle type={"server"} />
  </HStack>
);

const ChatApp: React.FC = () => {
  const [isSaveSwitchEnabled, setIsSaveSwitchEnabled] = useState(false);
  const [isWarnSwitchEnabled, setIsWarnSwitchEnabled] = useState(false);

  const [messages, setMessages] = useState<IMessage[]>([]);
  const [userMessage, setUserMessage] = useState<IMessage[]>([]);
  const [inputMessage, setInputMessage] = useState<string>("");
  const [loading, setLoading] = useState(false);
  // 將Set轉換為數組
  const list = new Set(["冰箱", "地下室", "冷氣", "房間", "加熱器", "電視"]);
  const arrayList = Array.from(list);
  // 生成隨機索引
  const randomIndex = Math.floor(Math.random() * arrayList.length);


  useEffect(() => {
    const interval = setInterval(() => {
      const newMessage: IMessage = {
        id: messages.length,
        content: `${new Date().toLocaleTimeString()}`,
        isUserMessage: false,
        type: "alert",
        randomApp: getList(),
      };
      if (isWarnSwitchEnabled) {
        setMessages((prevMessages) => [...prevMessages, newMessage]);
      }
    }, 1000); // 每分钟新增一条消息

    return () => clearInterval(interval); // 清除interval
  }, [messages, isWarnSwitchEnabled]);

  useEffect(() => {
    const interval = setInterval(() => {
      const newMessage: IMessage = {
        id: messages.length,
        content: `${new Date().toLocaleTimeString()}`,
        isUserMessage: false,
        type: "save",
        randomApp: getList(),
      };
      if (isSaveSwitchEnabled) {
        setMessages((prevMessages) => [...prevMessages, newMessage]);
      }
    }, 1000); // 每分钟新增一条消息

    return () => clearInterval(interval); // 清除interval
  }, [messages, isSaveSwitchEnabled]);

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
        const entityMessages = data.entities.map(
          (entity: any) => `${entity[0]}: ${entity[1]}`
        );
        const NERMessage: IMessage = {
          id: messages.length,
          content: "{\n" + entityMessages.join("\n") + "\n}",
          isUserMessage: false,
        };
        // setMessages([...messages, NERMessage]);
        const newMessage: IMessage = {
          id: messages.length,
          content: data.message,
          isUserMessage: false,
        };

        // 異常
        const newMessage2: IMessage = {
          id: messages.length,
          content: data.ano,
          isUserMessage: false,
          color: data.ano === "有異常" ? "#f00" : "#000",
        };

        // 添加
        let append = [];
        if (data.ano === "有異常")
          append = [...messages, NERMessage, newMessage, newMessage2];
        else append = [...messages, NERMessage, newMessage];

        setMessages(append);
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
  const now = new Date();
  const formattedDate = now.toLocaleDateString(); // 根據當前地區設置格式化日期
  const formattedTime = now.toLocaleTimeString(); // 根據當前地區設置格式化時間

  const getList = () => {
    // 生成隨機索引
    const randomIndex = Math.floor(Math.random() * arrayList.length);

    // 根據隨機索引取出對應的元素
    const randomElement = arrayList[randomIndex];
    return randomElement;
  };
  return (
    <Container flex={1} {...styles.wh100} w={"100%"}>
      <Header
        isSaveSwitchEnabled={isSaveSwitchEnabled}
        setIsSaveSwitchEnabled={setIsSaveSwitchEnabled}
        isWarnSwitchEnabled={isWarnSwitchEnabled}
        setIsWarnSwitchEnabled={setIsWarnSwitchEnabled}
      />
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
                bg={
                  message.isUserMessage
                    ? "#5FD3FF"
                    : message.type === "alert"
                    ? "error.100"
                    : message.type === "save"
                    ? "success.50"
                    : "#fff"
                }
                borderRadius={5}
                p={2}
                ml={message.isUserMessage ? "auto" : 0}
                mr={!message.isUserMessage ? "auto" : 0}
                position="relative"
              >
                {message.type === "alert" || message.type === "save" ? (
                  <VStack>
                    <HStack space={3} alignContent={"center"}>
                      {message.type === "alert" ? (
                        <WarningTwoIcon color="#f00" size="6" />
                      ) : (
                        <SunIcon size="6" color="success.500" />
                      )}
                      <Text
                        color={
                          message.type === "alert" ? "#f00" : "success.500"
                        }
                        fontSize={"2xl"}
                        bold
                      >
                        {message.type === "alert" ? "用電異常" : "節約提醒"}
                      </Text>
                    </HStack>
                    <Text>
                      {message.content}
                    </Text>
                    <Box>
                      {message.type === "alert" ? (
                        <HStack>
                          <Text fontSize={"xl"}>發現</Text>
                          <Text bold fontSize={"xl"}>
                            {message.randomApp}
                          </Text>
                          <Text fontSize={"xl"}>狀況異常，請儘速查看</Text>
                        </HStack>
                      ) : (
                        <VStack>
                          <Text bold color={'teal.900'} fontSize={'xl'}>{message.randomApp} </Text>
                          <Text fontSize={"xl"}>
                            根據數據計算，此時通常為關閉狀態，是否關閉以節省能源？
                          </Text>
                          <Text bold fontSize={"xl"}>
                           
                          </Text>
                        </VStack>
                      )}
                    </Box>
                    
                  </VStack>
                ) : (
                  <Text fontSize={"lg"} color={message.color}>
                    {message.content}
                    <Triangle
                      type={message.isUserMessage ? "user" : "server"}
                    />
                  </Text>
                )}
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
