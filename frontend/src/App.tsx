import React, { useState, useEffect } from "react";
import "./App.css";
import { NativeBaseProvider, Box, Text, Container } from "native-base";
// import { colors } from "@styles/index";
// import ChatApp from "@screen/Chat";
import ChatApp from "./screen/Chat";

interface IData {
  members: string[];
}

const App: React.FC = () => {
  const [data, setData] = useState<IData[]>([]);
  const containerStyle = {
    width: "100%",
    height: "100%",
    maxWidth: "100%",
  };

  const wh100 = {
    flex: 1,
    width: "100%",
  };

  useEffect(() => {
    fetch("http://127.0.0.1:5000/members")
      .then((res) => res.json())
      .then((data) => {
        setData([data]);
        console.log(data);
      })
      .catch((e) => {
        console.log(e);
      });
  }, []);

  return (
    <NativeBaseProvider>
      {/* <Container safeArea {...containerStyle} flex={1}> */}
      <Container safeArea {...containerStyle} >
        <ChatApp />
      </Container>
      {/* <Box>Hello world</Box>
      {data.length === 0 ? (
          <Text> loading ... </Text>
        ) : (
          data[0].members.map((member, i) => (
            <Text key={i}>{member}</Text>
          ))
        )} */}
    </NativeBaseProvider>
  );
};

export default App;
