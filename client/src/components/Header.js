import React from 'react'
import './Header.css';

export default function Header() {
    const date = new Date();
    const options = {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        timeZone: 'UTC',
        timeZoneName: 'short'
    };
    const formattedDate = new Intl.DateTimeFormat('en-US', options).format(date);

  return (
    <div className='header-main'>
        <p className='header-conversion-txt'> 1GBP = 108.42 INR</p>
        <p className='header-date-txt'>  {formattedDate}</p>
    </div>
  )
}
