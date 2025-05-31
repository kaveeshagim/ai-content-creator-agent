declare module "react-calendar-heatmap" {
  import * as React from "react";

  export interface HeatmapValue {
    date: string;
    count?: number;
  }

  export interface CalendarHeatmapProps {
    startDate: Date | string;
    endDate: Date | string;
    values: HeatmapValue[];
    classForValue?: (value: HeatmapValue) => string;
    tooltipDataAttrs?: (value: HeatmapValue) => object;
    showWeekdayLabels?: boolean;
    onClick?: (value: HeatmapValue) => void;
    gutterSize?: number;
    horizontal?: boolean;
  }

  export default class CalendarHeatmap extends React.Component<CalendarHeatmapProps> {}
}
