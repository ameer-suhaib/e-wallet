import * as React from 'react';
import { DemoContainer } from '@mui/x-date-pickers/internals/demo';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { Dayjs } from 'dayjs';

interface BasicDatePickerProps {
  onChange: (date: Dayjs | null) => void;
}

export default function BasicDatePicker({ onChange }: BasicDatePickerProps) {
  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <DemoContainer components={['DatePicker']}>
        <DatePicker
          label="Select the starting date"
          onChange={onChange} // Pass onChange prop to DatePicker
        />
      </DemoContainer>
    </LocalizationProvider>
  );
}
