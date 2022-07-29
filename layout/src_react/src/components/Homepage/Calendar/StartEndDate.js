import React from 'react';
import DateInput from './DateInput';

const StartEndDate = ({ selectStartDate, selectEndDate}) => {
  return (
    <div className='start-end-date'>
      <DateInput type='Start' selectDate={selectStartDate}/>
      <div className="input-format" >
        <div className="input-style"></div>
      </div>
      <DateInput type='End' selectDate={selectEndDate}/>
    </div>
  );
};

export default StartEndDate;
