import React from "react";
import {
  Container,
  View,
  Input,
  Avatar,
  Text,
  HStack,
  VStack,
  Box,
} from "native-base";
import * as styles from "@styles/index";

const Header: React.FC = () => {
  return (
    <View flex={1} {...styles.wh100}>
      <HStack
        alignItems={"center"}
        {...styles.wh100}
        px={10}
        justifyContent={"space-between"}
      >
        <VStack justifyContent={'center'}>
          <Text fontSize={"2xl"} bold>
            NLPowerAssistant
          </Text>
          <HStack alignItems={"center"} space={2}>
            <Text color={"#5FD3FF"} fontSize={"lg"}>
              Online
            </Text>
            <Box w={3} h={3} bg={'success.400'}  rounded={'full'}/>
          </HStack>
        </VStack>
        <Avatar
          bg="green.500"
          source={{
            uri: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80",
          }}
          size="lg"
        />
      </HStack>
    </View>
  );
};

export default Header;
