// src/components/RandomTextBox.js
import React from 'react';

const RandomTextBox = ({ randomData, randomTextEndRef }) => {
  return (
    <div className="random-text-box">
      <h2 className="info-title">Deal with feedback</h2>
      <div className="random-text-list">
        {randomData.split('\n').map((text, index) => (
          <p key={index}>{text}</p>
        ))}
        <div ref={randomTextEndRef} />
      </div>
    </div>
  );
};

export default RandomTextBox;
