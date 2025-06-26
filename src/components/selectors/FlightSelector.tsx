import React, {useState} from 'react';
import {AutoComplete, message, type SelectProps} from 'antd';
import {FlightService} from '@/services/FlightService.ts';
import type {autocompleteFlightIdResp} from '@/api/flightapi.ts';

interface FlightSelectorProps {
    value?: string;
    onChange?: (flightId: string, flightInfo: autocompleteFlightIdResp) => void;
    placeholder?: string;
    disabled?: boolean;
}

const FlightSelector: React.FC<FlightSelectorProps> = ({
                                                           value,
                                                           onChange,
                                                           placeholder = "请输入航班ID或飞机名称",
                                                           disabled = false
                                                       }) => {
    const [options, setOptions] = useState<{ value: string; label: string; data: autocompleteFlightIdResp }[]>([]);

    const handleSearch = async (searchText: string) => {
        if (!searchText) {
            setOptions([]);
            return;
        }

        try {
            const result = await FlightService.autocompleteFlightId(searchText);
            if (result) {
                const newOptions = result.map(flight => {
                    return {
                        label: `${flight.flight_id}(${flight.aircraft_name})`,
                        value: flight.flight_id,
                        data: flight
                    }
                })
                setOptions(newOptions);
            } else {
                setOptions([]);
            }
        } catch (error) {
            console.error('搜索航班失败:', error);
            message.error('搜索航班失败');
            setOptions([]);
        } finally {

        }
    };

    const handleSelect = (selectedValue: string) => {
        const selectedOption = options.find(option => option.value === selectedValue);
        if (selectedOption && onChange) {
            onChange(selectedValue, selectedOption.data);
        }
    };

    return (
        <AutoComplete
            value={value}
            options={options}
            onSearch={handleSearch}
            onSelect={handleSelect}
            placeholder={placeholder}
            disabled={disabled}

            allowClear
            showSearch
            filterOption={false}
            style={{width: '100%'}}
        />
    );
};

export default FlightSelector;