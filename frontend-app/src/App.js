import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, useNavigate } from "react-router-dom";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import Box from "@mui/material/Box";
import Drawer from "@mui/material/Drawer";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import List from "@mui/material/List";
import Typography from "@mui/material/Typography";
import Divider from "@mui/material/Divider";
import IconButton from "@mui/material/IconButton";
import MenuIcon from "@mui/icons-material/Menu";
import ChevronLeftIcon from "@mui/icons-material/ChevronLeft";
import AddIcon from "@mui/icons-material/Add";
import ChatIcon from "@mui/icons-material/Chat";
import LoginIcon from "@mui/icons-material/Login";
import LogoutIcon from "@mui/icons-material/Logout";
import PersonAddIcon from "@mui/icons-material/PersonAdd";
import ListItem from "@mui/material/ListItem";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";
import { format } from "date-fns";
import Chatbot from "./Chatbot";

const drawerWidth = 280;

const theme = createTheme({
  palette: {
    primary: { main: "#FF9933" },
    secondary: { main: "#800080" },
    background: { default: "#FFFFFF", paper: "#FFF8DC" },
  },
  typography: {
    fontFamily: '"Poppins", "Roboto", "Helvetica", "Arial", sans-serif',
    h6: { fontWeight: 600 },
  },
});

function AppContent() {
  const [open, setOpen] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [chats, setChats] = useState(() => {
    const savedChats = localStorage.getItem("ramayanChats");
    return savedChats ? JSON.parse(savedChats) : [];
  });
  const [selectedChatId, setSelectedChatId] = useState(null);
  const navigate = useNavigate();

  const handleDrawerOpen = () => setOpen(true);
  const handleDrawerClose = () => setOpen(false);

  const handleLogout = () => {
    setIsAuthenticated(false);
    navigate("/");
  };

  const handleNewChat = () => {
    const newChat = {
      id: Date.now(),
      title: "New Chat",
      createdAt: new Date().toISOString(),
      messages: [], // Start with an empty message history
    };
    const updatedChats = [newChat, ...chats];
    setChats(updatedChats);
    setSelectedChatId(newChat.id); // Set the new chat as the selected chat
    localStorage.setItem("ramayanChats", JSON.stringify(updatedChats)); // Save to localStorage
    navigate("/chat");
    handleDrawerClose();
  };

  const handleSelectChat = (chatId) => {
    setSelectedChatId(chatId);
    navigate("/chat");
    handleDrawerClose();
  };

  const getSelectedChat = () => chats.find((chat) => chat.id === selectedChatId);

  // Save chats to localStorage whenever they change
  useEffect(() => {
    localStorage.setItem("ramayanChats", JSON.stringify(chats));
  }, [chats]);

  return (
    <Box sx={{ display: "flex", minHeight: "100vh" }}>
      <AppBar
        position="fixed"
        sx={{
          zIndex: (theme) => theme.zIndex.drawer + 1,
          background: "linear-gradient(45deg, #FF9933 30%, #FFB366 90%)",
          boxShadow: "0 2px 4px rgba(0,0,0,0.2)",
        }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            onClick={handleDrawerOpen}
            edge="start"
            sx={{ mr: 2, ...(open && { display: "none" }) }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" sx={{ flexGrow: 1, fontWeight: 600 }}>
            Ramayan Chatbot
          </Typography>
          {!isAuthenticated ? (
            <>
              <IconButton color="inherit" onClick={() => setIsAuthenticated(true)}>
                <LoginIcon />
              </IconButton>
              <IconButton color="inherit">
                <PersonAddIcon />
              </IconButton>
            </>
          ) : (
            <IconButton color="inherit" onClick={handleLogout}>
              <LogoutIcon />
            </IconButton>
          )}
        </Toolbar>
      </AppBar>

      <Drawer
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          "& .MuiDrawer-paper": {
            width: drawerWidth,
            boxSizing: "border-box",
            backgroundColor: "#FFF8DC",
            borderRight: "2px solid #FF9933",
          },
        }}
        variant="persistent"
        anchor="left"
        open={open}
      >
        <Toolbar>
          <IconButton onClick={handleDrawerClose} sx={{ color: "#FF9933" }}>
            <ChevronLeftIcon />
          </IconButton>
        </Toolbar>
        <Divider sx={{ borderColor: "#FF9933" }} />
        <List>
          <ListItem button onClick={handleNewChat}>
            <ListItemIcon>
              <AddIcon sx={{ color: "#FF9933" }} />
            </ListItemIcon>
            <ListItemText primary="New Chat" sx={{ color: "#800080", fontWeight: 500 }} />
          </ListItem>
        </List>
        <Divider sx={{ borderColor: "#FF9933" }} />
        <List>
          {chats.map((chat) => (
            <ListItem
              key={chat.id}
              button
              selected={selectedChatId === chat.id}
              onClick={() => handleSelectChat(chat.id)}
              sx={{
                "&:hover": { backgroundColor: "rgba(255, 153, 51, 0.1)" },
                "&.Mui-selected": { backgroundColor: "rgba(255, 153, 51, 0.2)" },
              }}
            >
              <ListItemIcon>
                <ChatIcon sx={{ color: "#FF9933" }} />
              </ListItemIcon>
              <ListItemText
                primary={
                  <Typography
                    variant="body2"
                    sx={{
                      color: "#800080",
                      fontWeight: selectedChatId === chat.id ? 600 : 400,
                      overflow: "hidden",
                      textOverflow: "ellipsis",
                      whiteSpace: "nowrap",
                    }}
                  >
                    {chat.title || "New Chat"}
                  </Typography>
                }
                secondary={
                  <Typography variant="caption" sx={{ color: "#666" }}>
                    {format(new Date(chat.createdAt), "MMM d, h:mm a")}
                  </Typography>
                }
              />
            </ListItem>
          ))}
        </List>
      </Drawer>

      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          mt: 8,
          backgroundColor: "#FFFFFF",
        }}
      >
        <Routes>
          <Route
            path="/"
            element={
              <Box sx={{ textAlign: "center", mt: 4 }}>
                <Typography variant="h4" sx={{ color: "#800080", fontWeight: 600 }}>
                  Welcome to Ramayan Chatbot
                </Typography>
                <Typography variant="body1" sx={{ mt: 2, color: "#4B0082" }}>
                  Ask questions about the Ramayan and get instant answers
                </Typography>
              </Box>
            }
          />
          <Route
            path="/chat"
            element={<Chatbot chat={getSelectedChat()} />} // Pass selected chat messages here
          />
        </Routes>
      </Box>
    </Box>
  );
}

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <AppContent />
      </Router>
    </ThemeProvider>
  );
}

export default App;
