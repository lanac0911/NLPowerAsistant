import React from "react";
import {
  Menu,
  View,
  SunIcon,
  Avatar,
  Text,
  HStack,
  VStack,
  Box,
  Pressable,
  useDisclose,
  HamburgerIcon,
  WarningOutlineIcon,
  Switch,
} from "native-base";
import * as styles from "@styles/index";

interface HeaderProps {
  isSaveSwitchEnabled: boolean;
  setIsSaveSwitchEnabled: React.Dispatch<React.SetStateAction<boolean>>;
  isWarnSwitchEnabled: boolean;
  setIsWarnSwitchEnabled: React.Dispatch<React.SetStateAction<boolean>>;
}

const Header: React.FC<HeaderProps>= ({
  isSaveSwitchEnabled,
  setIsSaveSwitchEnabled,
  isWarnSwitchEnabled,
  setIsWarnSwitchEnabled,
}) => {
  const { isOpen, onToggle } = useDisclose();
  return (
    <View flex={1} {...styles.wh100}>
      <HStack
        alignItems={"center"}
        {...styles.wh100}
        px={10}
        justifyContent={"space-between"}
      >
        <VStack justifyContent={"center"}>
          <Text fontSize={"2xl"} bold>
            NLPowerAssistant
          </Text>
          <HStack alignItems={"center"} space={2}>
            <Text color={"#5FD3FF"} fontSize={"lg"}>
              Online
            </Text>
            <Box w={3} h={3} bg={"success.400"} rounded={"full"} />
          </HStack>
        </VStack>

        <Avatar
          bg="green.500"
          source={{
            uri: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80",
          }}
          size="lg"
        />

        <Menu
          w="230"
          right={35}
          trigger={(triggerProps) => {
            return (
              <Pressable
                accessibilityLabel="More options menu"
                {...triggerProps}
              >
                <HamburgerIcon />
              </Pressable>
            );
          }}
        >
          <Menu.Item isDisabled>
            <WarningOutlineIcon color={"warning.400"} />
            <Text fontSize={"lg"} color={"warning.400"}>
              警告提示
            </Text>
            <Switch
              offTrackColor="warning.100"
              onTrackColor="warning.200"
              onThumbColor="warning.500"
              offThumbColor="warning.50"
              isChecked={isWarnSwitchEnabled}
              onToggle={setIsWarnSwitchEnabled}
            />
          </Menu.Item>
          <Menu.Item isDisabled>
            <SunIcon color={"teal.600"} />
            <Text fontSize={"lg"} color={"teal.600"}>
              節約提示
            </Text>
            <Switch
              offTrackColor="teal.100"
              onTrackColor="teal.200"
              onThumbColor="teal.500"
              offThumbColor="teal.50"
              isChecked={isSaveSwitchEnabled}
              onToggle={setIsSaveSwitchEnabled}
            />
          </Menu.Item>
        </Menu>
      </HStack>
    </View>
  );
};

export default Header;
