import dayjs from 'dayjs';
import utc from 'dayjs/plugin/utc';
import timezone from 'dayjs/plugin/timezone';

dayjs.extend(utc);
dayjs.extend(timezone);

/**
 * 将本地时间转换为ISO格式（带时区信息）
 * @param date - dayjs对象或字符串
 * @returns ISO格式字符串
 */
export const formatLocalDateToISO = (date: any): string => {
    if (!date) return '';
    return dayjs(date).toISOString();
};

/**
 * 将GMT格式时间转换为本地时间显示
 * @param gmtDate - GMT格式时间字符串 (如: "Fri, 25 Apr 2025 00:00:00 GMT")
 * @returns 本地时间字符串
 */
export const formatGMTDateToLocal = (gmtDate: string): string => {
    if (!gmtDate) return '';
    try {
        // 解析GMT时间并转换为本地时间
        const localDate = dayjs(gmtDate).local();
        return localDate.format('YYYY-MM-DD HH:mm:ss');
    } catch (error) {
        console.error('日期格式转换失败:', error);
        return gmtDate;
    }
};

/**
 * 将UTC时间转换为本地时间显示
 * @param utcDate - UTC时间字符串 (如: "2025-06-10T00:00:00")
 * @returns 本地时间字符串
 */
export const formatUTCToLocal = (utcDate: string): string => {
    if (!utcDate) return '';
    try {
        const localDate = dayjs.utc(utcDate).local();
        return localDate.format('YYYY-MM-DD HH:mm:ss');
    } catch (error) {
        console.error('UTC日期转换失败:', error);
        return utcDate;
    }
};

/**
 * 获取当前时区
 */
export const getCurrentTimezone = (): string => {
    return dayjs.tz.guess();
};

/**
 * 格式化日期显示
 * @param date - 日期
 * @param format - 格式化模板
 */
export const formatDate = (date: any, format: string = 'YYYY-MM-DD HH:mm:ss'): string => {
    if (!date) return '';
    return dayjs(date).format(format);
};