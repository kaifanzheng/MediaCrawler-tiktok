import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

const CrackingPointer = ({ start }) => {
  const svgRef = useRef();
  const intervalRef = useRef();

  useEffect(() => {
    const svgWidth = 500;
    const svgHeight = 300;
    const radius = Math.min(svgWidth, svgHeight) / 3;
    const centerX = svgWidth / 2;
    const centerY = svgHeight / 2;

    const svg = d3.select(svgRef.current)
      .attr('width', svgWidth)
      .attr('height', svgHeight)
      .style('background', '#000')
      .style('overflow', 'visible');

    // Clear previous content
    svg.selectAll("*").remove();

    // Create a border for the svg
    svg.append('rect')
      .attr('width', svgWidth)
      .attr('height', svgHeight)
      .attr('stroke', '#b9b9b9')
      .attr('fill', 'none');

    // Add title
    svg.append('text')
      .attr('x', svgWidth / 2)
      .attr('y', 20)
      .attr('text-anchor', 'middle')
      .attr('fill', '#b9b9b9')
      .text('Cracking pointer');

    // Create the compass circle
    svg.append('circle')
      .attr('cx', centerX)
      .attr('cy', centerY)
      .attr('r', radius)
      .attr('stroke', '#b9b9b9')
      .attr('fill', 'none');

    // Create the pointer
    const pointer = svg.append('line')
      .attr('x1', centerX)
      .attr('y1', centerY)
      .attr('x2', centerX)
      .attr('y2', centerY - radius)
      .attr('stroke', '#b9b9b9')
      .attr('stroke-width', 2);

    const update = () => {
      const angle = Math.random() * 360;
      pointer.attr('transform', `rotate(${angle}, ${centerX}, ${centerY})`);
    };

    if (start) {
      intervalRef.current = setInterval(update, 500 + Math.random() * 1500);
    } else {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
      pointer.attr('transform', `rotate(0, ${centerX}, ${centerY})`); // Reset pointer position
    }

    return () => {
      clearInterval(intervalRef.current);
    };
  }, [start]);

  return <svg ref={svgRef}></svg>;
};

export default CrackingPointer;
