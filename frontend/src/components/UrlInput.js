import React from 'react';

const UrlInput = ({ url, setUrl }) => (
  <div className="url-input-container">
    <input
      className="url-input"
      type="text"
      value={url}
      onChange={(e) => setUrl(e.target.value)}
      placeholder="请输入直播间URL"
    />
  </div>
);

export default UrlInput;
