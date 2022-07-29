import React from 'react';

const DateInput = ({ type, selectDate }) => {
  const onChangeDate = (e) => {
   selectDate(e.target.value)
  }

  return (
    <div className='date-input'>
      <div className='date-font'>{`${type} Date`}</div>
      <input className='chooose-date' type='date' onChange={onChangeDate}/>
    </div>
  );
};

export default DateInput;
