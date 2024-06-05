// src/components/InfoBox.js
import React from 'react';

const InfoBox = ({ usernames, usernamesEndRef }) => {
  return (
    <div className="info-box">
      <h2 className="info-title">Crawl users</h2>
      <div className="usernames-list">
        {usernames.map((username, index) => (
          <p key={index}>{username}</p>
        ))}
        <div ref={usernamesEndRef} />
      </div>
    </div>
  );
};

export default InfoBox;
