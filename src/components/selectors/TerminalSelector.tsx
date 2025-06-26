
import React, { useCallback, useMemo } from 'react';
import { Select, type SelectProps } from 'antd';
import { useTerminalStore } from '../../store/terminal/terminalStore.ts';
import { TerminalService } from '../../services/TerminalService.ts';

interface TerminalSelectorProps extends Omit<SelectProps, 'options' | 'loading'> {
    onSearchError?: (error: any) => void;
}

export const TerminalSelector: React.FC<TerminalSelectorProps> = ({
                                                                      onSearchError,
                                                                      onFocus,
                                                                      onSearch,
                                                                      ...selectProps
                                                                  }) => {
    const { terminals } = useTerminalStore();
    const [loading, setLoading] = React.useState(false);

    // 搜索航站楼
    const searchTerminal = useCallback(async (searchValue: string) => {
        setLoading(true);
        try {
            await TerminalService.getTerminalList({
                terminal_name: searchValue || null,
                description: null
            });
        } catch (error) {
            console.error('搜索航站楼失败:', error);
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
                // @ts-ignore
                timeoutId = setTimeout(() => {
                    searchTerminal(value);
                }, 300);
            };
        },
        [searchTerminal]
    );

    // 处理焦点事件
    const handleFocus = useCallback((e: React.FocusEvent<HTMLElement>) => {
        // 如果没有数据，则加载初始数据
        if (terminals.length === 0) {
            searchTerminal('');
        }
        onFocus?.(e);
    }, [terminals.length, searchTerminal, onFocus]);

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
            options={terminals.map(terminal => ({
                value: terminal.terminal_id,
                label: terminal.terminal_name,
                key: terminal.terminal_id
            }))}
        />
    );
};