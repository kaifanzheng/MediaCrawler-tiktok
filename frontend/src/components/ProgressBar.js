// frontend/src/components/ProgressBar.js
import React, { useState, useEffect } from 'react';
import '../App.css';

const ProgressBar = ({ isLoading }) => {
  const messages = ["破译中..", "抓取中..", "算法重构中..","监测到反爬","正在分析数据","fetching data.."];
  const [currentMessage, setCurrentMessage] = useState(messages[0]);
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    if (isLoading) {
      const updateProgress = () => {
        const nextProgress = Math.min(progress + Math.random() * 10, 100);
        setProgress(nextProgress);
        if (nextProgress < 100) {
          const nextMessage = messages[Math.floor(Math.random() * messages.length)];
          setCurrentMessage(nextMessage);
          setTimeout(updateProgress, Math.floor(Math.random() * 2000) + 1000);
        }
      };
      updateProgress();
    } else {
      setProgress(0);
    }
  }, [isLoading]);

  return (
    isLoading && (
      <div className="progress-bar-container">
        <div className="progress-bar">
          {currentMessage}
          <div className="progress-bar-inner" style={{ width: `${progress}%` }} />
        </div>
      </div>
    )
  );
};

export default ProgressBar;
