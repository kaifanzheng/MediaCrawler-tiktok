// frontend/src/components/ButtonGroup.js
import React from 'react';

const ButtonGroup = ({ handleStart, handlePause, handleExport, canExport, messageCount }) => (
  <div className="button-container">
    <button onClick={handleStart}>Start</button>
    <button onClick={handlePause}>Pause</button>
    <button 
      onClick={handleExport} 
      disabled={!canExport} 
      style={{ backgroundColor: canExport ? 'black' : 'red', color: 'white' }}
    >
      Export
    </button>
  </div>
);

export default ButtonGroup;
