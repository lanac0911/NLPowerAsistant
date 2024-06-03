import React from "react";
import { Box } from "native-base";

interface TriangleProps {
  type: "user" | "server";
}

const Triangle: React.FC<TriangleProps> = ({ type }) => {
  return (
    <Box
      position="absolute"
      top={-5}
      right={type === "user" ? -5 : undefined} // 根据消息类型设置right值
      left={type === "server" ? -5 : undefined} // 根据消息类型设置left值
      width={0}
      height={0}
      borderTopWidth={9}
      borderTopColor={type === "server" ? "#fff" : "#5FD3FF"}
      borderRightWidth={type === "server" ? 9 : 0}
      borderRightColor="transparent"
      borderLeftWidth={type === "user" ? 9 : 0}
      borderLeftColor={type === "user" ? "transparent" : "none"}
    />
  );
};

export default Triangle;
