import React, { useState } from 'react';
import { AutoComplete } from 'antd';
import {AircraftListService} from "../../../services/AircraftListService.ts";
import {useAircraftStore} from "../../../store/aircraft/aircraftStore.ts";


interface AircraftSelectorProps {
    value?: string;
    onChange?: (value: string, option?: any) => void;
    placeholder?: string;
    required?: boolean;
    disabled?: boolean;
}

const AircraftSelector: React.FC<AircraftSelectorProps> = ({
                                                               value,
                                                               onChange,
                                                               placeholder = "请选择飞机",
                                                               required = false,
                                                               disabled = false
                                                           }) => {
    const [aircraftOptions, setAircraftOptions] = useState<Array<{
        value: string;
        label: string;
        aircraft_id: string;
    }>>([]);
    const [searching, setSearching] = useState(false);

    const handleSearch = async (searchText: string) => {
        if (!searchText || searchText.length < 2) {
            setAircraftOptions([]);
            return;
        }

        setSearching(true);
        try {
            // 使用 AircraftListService 搜索飞机
            await AircraftListService.getAircraftList({
                aircraft_name: searchText,
                age: null,
                type_name: null,
                description: null
            });

            // 从 store 中获取搜索结果
            const { aircrafts } = useAircraftStore.getState();

            const options = aircrafts.map((aircraft: any) => ({
                value: aircraft.aircraft_name,
                label: aircraft.aircraft_name,
                aircraft_id: aircraft.aircraft_id
            }));

            setAircraftOptions(options);
        } catch (error) {
            console.error('搜索飞机失败:', error);
            setAircraftOptions([]);
        } finally {
            setSearching(false);
        }
    };

    const handleSelect = (selectedValue: string, option: any) => {
        if (onChange) {
            // 传递 aircraft_id 而不是 aircraft_name
            onChange(option.aircraft_id, option);
        }
    };

    const handleChange = (changedValue: string) => {
        if (!changedValue && onChange) {
            onChange('');
        }
    };

    return (
        <AutoComplete
            value={value}
            placeholder={placeholder}
            style={{ width: '100%' }}
            options={aircraftOptions}
            onSearch={handleSearch}
            onSelect={handleSelect}
            onChange={handleChange}
            notFoundContent={searching ? '搜索中...' : '输入至少2个字符开始搜索'}
            allowClear
            disabled={disabled}
            filterOption={false}
        />
    );
};

export default AircraftSelector;