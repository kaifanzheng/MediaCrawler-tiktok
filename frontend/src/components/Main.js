// frontend/src/components/Main.js
import React, { useState, useEffect, useRef, useCallback } from 'react';
import '../App.css';
import ButtonGroup from './ButtonGroup';
import InfoBox from './InfoBox';
import RandomTextBox from './RandomTextBox';
import UrlInput from './UrlInput';
import CrackingFrequency from './CrackingFrequency';
import CrackingPointer from './CrackingPointer';
import ProgressBar from './ProgressBar'; // 引入进度条组件
import useWebSocket from '../hooks/useWebSocket';
import { fetchRandomText } from '../utils/fetchRandomText';
import { startScraping, startScraper, pauseScraping, downloadExcel } from '../services/api';

const Main = () => {
  const [url, setUrl] = useState('');
  const [start, setStart] = useState(false);
  const [shouldStartComponents, setShouldStartComponents] = useState(false);
  const [usernames, setUsernames] = useState([]);
  const [randomData, setRandomData] = useState('');
  const [canExport, setCanExport] = useState(false); // 是否可以导出的状态
  const [isLoading, setIsLoading] = useState(false); // 新增状态变量
  const usernamesEndRef = useRef(null);
  const randomTextEndRef = useRef(null);
  const [messageCount, setMessageCount] = useState(0);
  const [randomThreshold, setRandomThreshold] = useState(3 + Math.floor(Math.random() * 4));

  const handleWebSocketMessage = useCallback((data) => {
    if (data.message !== 'pong') {
      setUsernames(prevUsernames => [...prevUsernames, data.message]);
      setMessageCount(prevCount => {
        const newCount = prevCount + 1;
        if (newCount >= 3) {
          setShouldStartComponents(true);
          setCanExport(true); // 设置可以导出
        }
        if (newCount >= randomThreshold) {
          fetchRandomText().then(text => {
            setRandomData(prevData => prevData + '\n' + text);
          });
          setRandomThreshold(3 + Math.floor(Math.random() * 4));
          return 0;
        }
        return newCount;
      });
    }
  }, []);

  useWebSocket('ws://localhost:8000/ws/users/', handleWebSocketMessage, start);

  const handleStart = async () => {
    const urlPattern = /^https:\/\/live\.douyin\.com\/\d+$/;
    if (!urlPattern.test(url)) {
      alert('请输入有效的直播间URL');
      return;
    }

    setStart(true);
    setShouldStartComponents(false);
    setCanExport(false); // 开始时重置导出状态
    try {
      await startScraping(url); // 原来开始按钮的逻辑
      await startScraper(); // 新的爬虫功能
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handlePause = async () => {
    setStart(false);
    setShouldStartComponents(false);

    try {
      // 发送暂停信号和用户名列表到后端
      await pauseScraping(usernames);

      // 清空用户名列表
      setUsernames([]);
      setRandomData('');
      setCanExport(false); // 重置可以导出状态
    } catch (error) {
      console.error('Error:', error);
    }

    console.log("Paused scraping users");
  };

  const handleExport = async () => {
    if (!canExport) {
      alert('无数据导出');
      return;
    }

    setIsLoading(true); // 设置加载状态

    // 触发暂停功能
    await handlePause();

    // 导出数据
    try {
      await downloadExcel();
      setMessageCount(0); // 重置计数
      setCanExport(false); // 重置可以导出状态
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setIsLoading(false); // 取消加载状态
    }
  };

  useEffect(() => {
    if (usernamesEndRef.current) {
      usernamesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [usernames]);

  useEffect(() => {
    if (randomTextEndRef.current) {
      randomTextEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [randomData]);

  return (
    <div className="main-container">
      <ProgressBar isLoading={isLoading} /> {/* 显示进度条 */}
      <div className="dashboard-container">
        <div className="row-container">
          <div className="chart-container">
            <CrackingFrequency start={shouldStartComponents} />
          </div>
          <div className="chart-container">
            <CrackingPointer start={shouldStartComponents} />
          </div>
          <ButtonGroup handleStart={handleStart} handlePause={handlePause} handleExport={handleExport} canExport={canExport} messageCount={messageCount} />
        </div>
        <div className="row-container">
          <InfoBox usernames={usernames} usernamesEndRef={usernamesEndRef} />
          <RandomTextBox randomData={randomData} randomTextEndRef={randomTextEndRef} />
        </div>
      </div>
      <UrlInput url={url} setUrl={setUrl} />
    </div>
  );
};

export default Main;
