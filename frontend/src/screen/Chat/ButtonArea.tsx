import React from "react";
import { HStack, Input, Button, Box, Image } from "native-base";
const sendIcon = require("@styles/images/Send icon.png");

interface IMessage {
  sendMessage: () => Promise<void>;
  inputMessage: string;
  setInputMessage: React.Dispatch<React.SetStateAction<string>>;
}

const ButtonArea: React.FC<IMessage> = ({
  sendMessage,
  inputMessage,
  setInputMessage,
}) => {
  return (
    <Box bg={"#54cffd54"} flex={0.3} w={"100%"} justifyContent={"end"}>
      <HStack bg={"#fff"} mx={6} rounded={"full"} mb={3}>
        <Input
          flex={4}
          px={5}
          variant={"unstyled"}
          rounded={"2xl"}
          size={'lg'}
          placeholder="輸入訊息..."
          value={inputMessage}
          onChangeText={(text: React.SetStateAction<string>) =>
            setInputMessage(text)
          }
        />
        <Button 
          disabled={inputMessage === '' ? true : false}
          borderWidth={1}
          borderLeftColor={"#c9c9c9"}
          borderColor={"transparent"}
          onPress={sendMessage}
          bg={"#fff"}
          rounded={"full"}
          leftIcon={<Image source={sendIcon} alt="image error" size="xs" />}
        />
      </HStack>
    </Box>
  );
};

export default ButtonArea;
