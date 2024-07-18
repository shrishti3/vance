import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
import axios from 'axios';
import "./ChartSection.css";
import Search from "../assets/search.svg";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const currentDate = new Date();
const unixTimestamp = Math.floor(currentDate.getTime() / 1000);
const oneMonthAgo = unixTimestamp - (30 * 24 * 60 * 60); // Subtract 30 days worth of seconds

const periods = {
  '1M': { start: oneMonthAgo, end: unixTimestamp }, // Last 1 month
  '3M': { start: oneMonthAgo - (90 * 24 * 60 * 60), end: unixTimestamp }, // Last 3 months
  '6M': { start: oneMonthAgo - (180 * 24 * 60 * 60), end: unixTimestamp }, // Last 6 months
  '1Y': { start: oneMonthAgo - (365 * 24 * 60 * 60), end: unixTimestamp },
};

const ChartSection = () => {
  const [visibleDataset, setVisibleDataset] = useState('1M');
  const [chartData, setChartData] = useState({ labels: [], datasets: [] });
  const [loading, setLoading] = useState(true);
console.log(visibleDataset);
  const fetchData = async (period) => {
    setLoading(true);
    try {
      const response = await axios.get(`http://127.0.0.1:5000/api/forex-data`, {
        params: {
          from: 'GBP',
          to: 'INR',
          period1: periods[period].start,
          period2: periods[period].end,
        },
      });
      const data = response.data;

      const labels = data.map(item => item.Date);
      const dataset = data.map(item => parseFloat(item['Close    Close price adjusted for splits.']));
      setChartData({
        labels: labels,
        datasets: [{
          label: '1M',
          data: dataset,
          fill: true,
          backgroundColor: 'rgb(188,182,241)',
          borderColor: 'rgb(188,182,241)',
        },
        {
            label: '3M',
            data: dataset,
            fill: true,
            backgroundColor: 'rgb(188,182,241)',
            borderColor: 'rgb(188,182,241)',
          },
          {
            label: '6M',
            data: dataset,
            fill:true,
            backgroundColor: 'rgb(188,182,241)',
            borderColor: 'rgb(188,182,241)',
          },
          {
            label: '1Y',
            data: dataset,
            fill: true,
            backgroundColor: 'rgb(188,182,241)',
            borderColor: 'rgb(188,182,241)',
          }],
      });
    } catch (error) {
      console.error("Error fetching data", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData(visibleDataset);
  }, [visibleDataset]);

  const options = {
    responsive: true,
    plugins: {
      legend: {
        onClick: (e, legendItem) => {
          setVisibleDataset(legendItem.text);
        },
        labels: {
          usePointStyle: true,
          pointStyle: 'line',
        },
      },
    },
  };

  return (
    <div>
      {loading ? (
        <div className="loader"><p className='loader-txt'>Loading...</p><img src={Search} className='loader-img' /></div>
      ) : (
        <Line data={chartData} options={options} className='chart-graph' />
      )}
    </div>
  );
};

export default ChartSection;
