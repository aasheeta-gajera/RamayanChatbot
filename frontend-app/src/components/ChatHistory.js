import React from 'react';
import { List, ListItem, ListItemText, ListItemIcon, Typography, Box } from '@mui/material';
import ChatIcon from '@mui/icons-material/Chat';
import { format } from 'date-fns';

function ChatHistory({ chats, onSelectChat, selectedChatId }) {
  return (
    <List>
      {chats.map((chat) => (
        <ListItem
          key={chat.id}
          button
          onClick={() => onSelectChat(chat.id)}
          selected={selectedChatId === chat.id}
          sx={{
            '&:hover': {
              backgroundColor: 'rgba(255, 153, 51, 0.1)',
            },
            '&.Mui-selected': {
              backgroundColor: 'rgba(255, 153, 51, 0.2)',
            },
          }}
        >
          <ListItemIcon>
            <ChatIcon sx={{ color: '#FF9933' }} />
          </ListItemIcon>
          <ListItemText
            primary={
              <Typography
                variant="body2"
                sx={{
                  color: '#800080',
                  fontWeight: selectedChatId === chat.id ? 600 : 400,
                  overflow: 'hidden',
                  textOverflow: 'ellipsis',
                  whiteSpace: 'nowrap',
                }}
              >
                {chat.title || 'New Chat'}
              </Typography>
            }
            secondary={
              <Typography
                variant="caption"
                sx={{ color: '#666' }}
              >
                {format(new Date(chat.createdAt), 'MMM d, h:mm a')}
              </Typography>
            }
          />
        </ListItem>
      ))}
    </List>
  );
}

export default ChatHistory; 