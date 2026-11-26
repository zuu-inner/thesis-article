import { render } from 'pele';

export interface RenderOptions {
    fontFamily?: string;
    fontSize?: number;
    padding?: number;
}

export interface RenderResult {
    svg: string;
    width: number;
    height: number;
    type: string;
}

export function renderDiagram(
    source: string,
    options: RenderOptions = {},
): RenderResult {
    const fontFamily =
        options.fontFamily ?? 'Arial, Helvetica, sans-serif';

    const result = render(source, {
        fontFamily,
        fontSize: options.fontSize ?? 14,
        padding: options.padding ?? 16,
        responsive: false,
        autoDirection: false,
    });

    return {
        svg: result.svg,
        width: result.width,
        height: result.height,
        type: result.type,
    };
}