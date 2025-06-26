import React, { useCallback, useMemo } from 'react';
import { Select, type SelectProps } from 'antd';
import { useAircraftStore } from '../../store/aircraft/aircraftStore.ts';
import { AircraftListService } from '../../services/AircraftListService.ts';

interface AircraftSelectorProps extends Omit<SelectProps, 'options' | 'loading'> {
    onSearchError?: (error: any) => void;
}

export const AircraftSelector: React.FC<AircraftSelectorProps> = ({
                                                                      onSearchError,
                                                                      onFocus,
                                                                      onSearch,
                                                                      ...selectProps
                                                                  }) => {
    const { aircrafts } = useAircraftStore();
    const [loading, setLoading] = React.useState(false);

    // 搜索飞机
    const searchAircraft = useCallback(async (searchValue: string) => {
        setLoading(true);
        try {
            await AircraftListService.getAircraftList({
                aircraft_name: searchValue || null,
                age: null,
                type_name: null,
                description: null
            });
        } catch (error) {
            console.error('搜索飞机失败:', error);
            onSearchError?.(error);
        } finally {
            setLoading(false);
        }
    }, [onSearchError]);

    // 防抖搜索
    const debouncedSearch = useMemo(
        () => {
            let timeoutId: number;
            return (value: string) => {
                clearTimeout(timeoutId);
                timeoutId = setTimeout(() => {
                    searchAircraft(value);
                }, 300);
            };
        },
        [searchAircraft]
    );

    // 处理焦点事件
    const handleFocus = useCallback((e: React.FocusEvent<HTMLElement>) => {
        // 如果没有数据，则加载初始数据
        if (aircrafts.length === 0) {
            searchAircraft('');
        }
        onFocus?.(e);
    }, [aircrafts.length, searchAircraft, onFocus]);

    // 处理搜索事件
    const handleSearch = useCallback((value: string) => {
        debouncedSearch(value);
        onSearch?.(value);
    }, [debouncedSearch, onSearch]);

    return (
        <Select
            {...selectProps}
            loading={loading}
            showSearch
            filterOption={false}
            onFocus={handleFocus}
            onSearch={handleSearch}
            options={aircrafts.map(aircraft => ({
                value: aircraft.aircraft_id,
                label: `${aircraft.aircraft_name} (${aircraft.type_name})`,
                key: aircraft.aircraft_id
            }))}
        />
    );
};