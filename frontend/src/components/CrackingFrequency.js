import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

const CrackingFrequency = ({ start }) => {
  const svgRef = useRef();
  const intervalRef = useRef();

  useEffect(() => {
    const svgWidth = 500;
    const svgHeight = 300;
    const padding = { top: 40, right: 40, bottom: 40, left: 40 };
    const width = svgWidth - padding.left - padding.right;
    const height = svgHeight - padding.top - padding.bottom;

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
      .attr('y', padding.top / 2)
      .attr('text-anchor', 'middle')
      .attr('fill', '#b9b9b9')
      .text('Cracking Frequency');

    // Scales
    const xScale = d3.scaleLinear()
      .domain([0, 40])
      .range([padding.left, width]);

    const yScale = d3.scaleLinear()
      .domain([1, 5])
      .range([height, padding.top]);

    // Axes
    const yAxis = d3.axisLeft(yScale).ticks(5);
    svg.append('g')
      .attr('transform', `translate(${padding.left}, 0)`)
      .call(yAxis)
      .selectAll("text")
      .attr("fill", "#b9b9b9");

    // Line generator
    const line = d3.line()
      .x((d, i) => xScale(i))
      .y(d => yScale(d))
      .curve(d3.curveCardinal);

    let data = [];

    const path = svg.append('path')
      .datum(data)
      .attr('fill', 'none')
      .attr('stroke', '#b9b9b9')
      .attr('stroke-width', 2)
      .attr('d', line);

    const update = () => {
      if (data.length >= 40) {
        data.shift();
      }
      data.push(Math.floor(Math.random() * 5) + 1);
      path.datum(data)
        .attr('d', line);
    };

    if (start) {
      data = []; // Reset data array
      intervalRef.current = setInterval(update, 500);
    } else {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
      data = []; // Clear data
      path.datum(data).attr('d', line); // Clear the path
    }

    return () => {
      clearInterval(intervalRef.current);
    };
  }, [start]);

  return <svg ref={svgRef}></svg>;
};

export default CrackingFrequency;
