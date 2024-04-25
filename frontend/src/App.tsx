import React, { useState, useEffect } from "react";
import "./App.css";
import { NativeBaseProvider, Box, Text } from "native-base";
import { colors } from "@styles/index";
interface IData {
  members: string[];
}

const App: React.FC = () => {
  const [data, setData] = useState<IData[]>([]);

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
      <Box>Hello world</Box>
      {data.length === 0 ? (
          <Text> loading ... </Text>
        ) : (
          data[0].members.map((member, i) => (
            <Text key={i}>{member}</Text>
          ))
        )}
    </NativeBaseProvider>
  );
};

export default App;
